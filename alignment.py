"""Find alignments between the VirtuosoNet dataset and the MAESTRO dataset"""
import argparse
import numpy as np
import pandas as pd
import sys
import pretty_midi
from pathlib import Path
import json



def get_midi_notes(midi, start=0):
    """
    Get a sorted list of all of the notes in a given MIDI file.
    
    Parameters
    ----------
    midi : PrettyMIDI
        A loaded MIDI file.
        
    start : float
        Notes that start earlier than this (in s) are not included in the return.
        
    Returns
    -------
    notes : np.ndarray
        An (N, 3) array, where the first column contains the start times (in s),
        second column contains end times (in s), and the 3rd column contains
        pitches. The rows will be sorted first by start time, and then by pitch.
    """
    # Get all notes, not necessarily in order
    notes_all = [[n.start, n.end, n.pitch]
                 for i in midi.instruments for n in i.notes if n.start >= start]
    # Order notes according to onset and pitch
    return np.array(sorted(notes_all, key = lambda x: (x[0],x[2])))



def normalize_midi_notes(notes):
    """
    Remove any initial silence from a given ndarray of notes.
    
    Parameters
    ----------
    notes : np.ndarray
        An (N, 3) array, where the first column contains the start times (in s),
        second column contains end times (in s), and the 3rd column contains
        pitches. The rows should be sorted first by start time, and then by pitch.
        
    Returns
    -------
    normalized_notes : np.ndarray
        The input notes array, after shifting the onset and offset times of each
        note so that the first note begins at time 0.
    """
    return notes - [notes[0][0], notes[0][0], 0]



def notes_are_similar(notes1, notes2, number_to_match=None, align_end=False, tol=0.03):
    """
    Test if two notes lists are the same, within some tolerance and up to some
    number of notes. Note start and end times are allowed some given tolerance,
    but pitches must be exact matches.
    
    Parameters
    ----------
    notes1 : np.ndarray
        An (N, 3) array, where the first column contains the start times (in s),
        second column contains end times (in s), and the 3rd column contains
        pitches. The rows should be sorted first by start time, and then by pitch.
        
    notes2 : np.ndarray
        Another notes array, of the same structure as notes1.
        
    number_to_match : int
        Check for matches on the first this many notes. If None, check all notes.
        
    align_end : boolean
        If True, align the ends of the two excerpts, and cut each note list to the length
        of the shorter one (by removing notes from the beginning of the long one).
        Then, perform the matching as usual, with number_to_match now counting
        back from the end.
        
    tol : float
        Note start and end times are allowed to differ by this much to be considered
        matches.
    
    Returns
    -------
    similar : boolean
        True if the two notes lists match up to the given number of ntoes and allowed
        tolerance. False otherwise.
    """
    if number_to_match is not None:
        if align_end:
            notes1 = notes1[-number_to_match:]
            notes2 = notes2[-number_to_match:]
        else:
            notes1 = notes1[:number_to_match]
            notes2 = notes2[:number_to_match]
        
    # Cut pieces to the same length with align_end
    if align_end:
        notes1 = normalize_midi_notes(notes1[-min(len(notes1), len(notes2)):])
        notes2 = normalize_midi_notes(notes2[-len(notes1):])
        
    # Here, the note lengths should be equal
    if len(notes1) != len(notes2):
        return False
    
    [onsets1, offsets1, pitches1] = np.split(notes1, 3, axis=1)
    [onsets2, offsets2, pitches2] = np.split(notes2, 3, axis=1)
    
    return (np.allclose(onsets1, onsets2, atol=tol) and
            np.allclose(offsets1, offsets2, atol=tol) and
            np.array_equal(pitches1, pitches2))



def find_match(vnet_row, maestro, vnet_notes, maestro_notes, matches, vnet_base='.',
               maestro_base='maestro', num_notes=None, align_end=False, verbose=False):
    """
    Find the match of a single row of the VirtuosoNet df, given
    a maestro df.
    
    Parameters
    ----------
    vnet_row : pd.Series
        A single row of the VirtuosoNet df, for which we are searching for a match.
        
    maestro : pd.DataFrame
        A pandas DataFrame containing all of the maestro entries to search through
        for a match.
        
    vnet_notes : dict
        A dictionary mapping each vnet row's index to a loaded ndarray of notes.
        
    maestro_notes : dict
        A dictionary mapping each maestro row's index to a loaded ndarray of notes.
        
    matches : dict
        A dictionary mapping each v_net row's index to the index of the matching
        maestro row.
        
    vnet_base : string
        The base directory for the VirtuosoNet data files.
        
    maestro_base : string
        The base directory for the MAESTRO data files.
        
    num_notes : int
        Check for matches on the first this many notes. If None, check all notes.
        
    align_end : boolean
        If True, align the ends of the two excerpts, and cut each note list to the length
        of the shorter one (by removing notes from the beginning of the long one).
        Then, perform the matching as usual, with number_to_match now counting
        back from the end.
        
    verbose : boolean
        Use verbose printing.
    """
    if verbose:
        print(f'Searching for matches to piece "{vnet_row.performed_midi_path}"')
        
    if vnet_row.name not in vnet_notes:
        vnet_notes[vnet_row.name] = normalize_midi_notes(get_midi_notes(
            pretty_midi.PrettyMIDI(str(Path(vnet_base, vnet_row.performed_midi_path)))
        ))
    vnet_row_notes = vnet_notes[vnet_row.name]
        
    for idx, maestro_row in maestro.iterrows():
        if idx not in maestro_notes:
            maestro_notes[idx] = normalize_midi_notes(get_midi_notes(
                pretty_midi.PrettyMIDI(str(Path(maestro_base, maestro_row.midi_filename)))
            ))
        maestro_row_notes = maestro_notes[idx]
        
        if notes_are_similar(vnet_row_notes, maestro_row_notes, number_to_match=num_notes,
                             align_end=align_end):
            if verbose:
                print(f'    Match found: "{maestro_row.midi_filename}"')
            if vnet_row.name not in matches:
                matches[vnet_row.name] = [idx]
            else:
                matches[vnet_row.name].append(idx)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate an alignment for VirtuosoNet'
                                     ' MIDI files to MAESTRO MIDI files.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('-vnd', '--virtuoso_net_dir', help='The path to the VirtuosoNet'
                        ' dataset files.', default='.')
    parser.add_argument('-vn', '--virtuoso_net', help='The path to the VirtuosoNet '
                        'data pickle file.', default='performance_dataframe.pkl',
                        type=pd.read_pickle)
    parser.add_argument('-md', '--maestro_dir', help='The path to the MAESTRO dataset '
                        'files.', default='maestro')
    parser.add_argument('-m', '--maestro', help='The path to the MAESTRO data json '
                        'file.', default='maestro-v2.0.0.json', type=pd.read_json)
    
    parser.add_argument('-c', '--composer', help='Search for alignment only within a '
                        'single VirtuosoNet composer.', default=None)
    
    parser.add_argument('-n', help='Check this many notes at the beginning of each piece.',
                        default=None, type=int)
    
    parser.add_argument('--end', help='Align the ends of the pieces when checking for match.',
                        action='store_true')
    
    parser.add_argument('-e', '--exhaustive', help='Search for alignment throughout the '
                        'full MAESTRO dataset for unmatched VirtuosoNet pieces. Otherwise,'
                        ' only search through MAESTRO pieces with closely-matched '
                        'composer names.', action='store_true')
    
    parser.add_argument('-o', '--output', help='Json output file to save the results.',
                        default='correspondence.json', type=Path)
    
    parser.add_argument('-v', '--verbose', help='Verbose printing.', action='store_true')
    
    args = parser.parse_args()
    
    
    v_net = args.virtuoso_net
    maestro = args.maestro
    
    # Filter V-Net by composer
    if args.composer is not None:
        v_net = pd.DataFrame(
            v_net.loc[args.virtuoso_net.author.str.lower() == args.composer.lower()]
        )
        if len(v_net) == 0:
            print(f'Error: No composer matching "{args.composer}" found in VirtuosoNet.',
                  file=sys.stderr)
            if args.verbose:
                print('Possible composers are:', file=sys.stderr)
                print(args.virtuoso_net.groupby('author').size(), file=sys.stderr)
            sys.exit(1)
                
    # Store notes outside of dataframe
    vnet_notes = {}
    maestro_notes = {}
    matches = {}
    
    # Initial search, only through matching MAESTRO composers
    # Still group V-net here by composer, to simplify code in case of no composer given
    for composer, group in v_net.groupby('author'):
        if args.verbose:
            print(f'Searching for matches to composer "{composer}", in closely-'
                  'matching MAESTRO composers.')
            print('The first piece will take longer as it must compute note data.')
            
        filtered_maestro = maestro.loc[
            maestro.canonical_composer.str.lower().str.contains(composer.lower())
        ]
        group.apply(find_match, axis=1, args=(filtered_maestro, vnet_notes,
                                              maestro_notes, matches),
                    vnet_base=args.virtuoso_net_dir, maestro_base=args.maestro_dir,
                    num_notes=args.n, align_end=args.end, verbose=args.verbose)
        
    if args.exhaustive:
        # Extended search through all MAESTRO pieces
        # No need to group V-net by composer here
        if args.verbose:
            print(f'Exhaustively searching MAESTRO for any unmatched pieces.')
            print('The first piece will take longer as it must compute note data.')

        # This saves and UNmatched composers (notice the '~')
        filtered_maestro = maestro.loc[
            ~maestro.canonical_composer.str.lower().str.contains(composer.lower())
        ]
        v_net_filtered = v_net.loc[~v_net.index.isin(matches)]
        v_net_filtered.apply(find_match, axis=1, args=(filtered_maestro, vnet_notes,
                                                       maestro_notes, matches),
                             vnet_base=args.virtuoso_net_dir, maestro_base=args.maestro_dir,
                             verbose=args.verbose)
        
    name_matches = {
        v_net.loc[key, 'performed_midi_path']: [maestro.loc[idx, 'midi_filename'] for idx in value]
        for key, value in matches.items()
    }
    
    multiple_vnet = [key for key, value in name_matches.items() if len(value) > 1]
    unmatched_vnet = list(v_net.loc[~v_net.index.isin(matches), 'performed_midi_path'])
    
    # Multiply matched MAESTRO pieces
    # Only check those which we searched
    maestro_match_counts = {key: 0 for key in maestro_notes}
    for idx_list in matches.values():
        for idx in idx_list:
            maestro_match_counts[idx] += 1
    multiple_maestro = [maestro.loc[idx, 'midi_filename']
                        for idx, count in maestro_match_counts.items() if count > 1]
    unmatched_maestro = [maestro.loc[idx, 'midi_filename']
                         for idx, count in maestro_match_counts.items() if count == 0]
    
    if args.verbose:
        print(f'ALL MATCHES ({len(name_matches)}):')
        print(name_matches)
        print()
        print(f'Multiply matched VirtuosoNet pieces ({len(multiple_vnet)}):')
        print('\n'.join(multiple_vnet))
        print()
        print(f'Unmatched VirtuosoNet pieces ({len(unmatched_vnet)}):')
        print('\n'.join(unmatched_vnet))
        print()
        print(f'Multiply matched MAESTRO pieces ({len(multiple_maestro)}):')
        print('\n'.join(multiple_maestro))
        print()
        print(f'Unmatched MAESTRO pieces ({len(unmatched_maestro)}):')
        print('\n'.join(unmatched_maestro))
    
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open(mode='w') as file:
        json.dump({'matches': name_matches,
                   'multiple_vnet': multiple_vnet,
                   'unmatched_vnet': unmatched_vnet,
                   'multiple_maestro': multiple_maestro,
                   'unmatched_maestro': unmatched_maestro},
                  file, indent=4, sort_keys=True)