# Performed midi dataset


The dataset contains 997 performances of 205 opus.


List of authors:
- Bach
- Balakirev
- Beethoven
- Brahms
- Chopin
- Debussy
- Glinka
- Haydn
- Liszt
- Mozart
- Prokofiev
- Rachmaninoff
- Ravel
- Schubert
- Schumann
- Scriabin

#### Objectives

Build a dataset containing
- XML score files 
- MIDI score
- MIDI performances
- down-beat / beat annotations (dates in performance)
- alignments between each event in the MIDI performance and the corresponding event in the XML score


#### Usage:
- ground truth for MIDI piano automatic music transcription (AMT) tasks
    - MIDI beat/downbeat tracking
    - MIDI quantization
    - voice separations
    - score structuring
- ground truth for piano expressive performance models
    

---
## Source Dataset
the dataset is obtained by curating the following dataset by Jeong et al.
(manual cleaning of the beat mark annotations)


- this dataset is used for the evalution of `VirtuosoNet` 
  https://github.com/jdasam/virtuosoNet
- the dataset is not public
- solo piano music, classical music, polyphonic, symbolic (MIDI + annote)

refs:


> Graph Neural Network for Music Score Data and Modeling Expressive Piano Performance
Dasaem Jeong, Taegyun Kwon, Yoojin Kim, Juhan Nam 
> Proceedings of the 36th International Conference on Machine Learning, PMLR 97:3060-3070, 2019.
> http://proceedings.mlr.press/v97/jeong19a.html


> VirtuosoNet: A Hierarchical Attention RNN for Generating Expressive Piano Performance from Music Score
> Dasaem Jeong, Taegyun Kwon, Juhan Nam
> NIPS 2018
> https://github.com/jdasam/virtuosoNet

> VirtuosoNet: A Hierarchical RNN-based System for Modeling Expressive Piano Performance  
> Dasaem Jeong; Taegyun Kwon; Yoojin Kim; Kyogu Lee; Juhan Nam
> ISMIR 2019
> http://archives.ismir.net/ismir2019/paper/000112.pdf

The dataset contains a set of performances from Yamaha competition 
(multiple performances of the same opus are present). The following files 
are associated to each performance:
- XML score from musescore in musicXML format
- MIDI score (quantified MIDI) produced with Musescore from the musicXML file, 
   duplicating the eventual repetitions in the score.
- alignement (txt file) between the performed midi and the score midi,
  obtained with the Nakamura algo below.
- alignment (txt file) between the performed midi and the xml score, 
  obtained with the Nakamura algo below.
  
> Performance Error Detection and Post-Processing for Fast and Accurate Symbolic Music Alignment  
> Eita Nakamura, Kazuyoshi Yoshii, Haruhiro Katayose
> ISMIR 2017
> https://eita-nakamura.github.io/articles/EN_etal_ErrorDetectionAndRealignment_ISMIR2017.pdf

---
#### dataset content and curation procedure

available at:  
https://github.com/fosfrancesco/performed-midi-dataset


The procedure is:
- Choose a Folder from the dataset (from authors above)
- Open Audacity https://www.audacityteam.org/
- File -> Import ->MIDI file: `midi_cleaned.mid`
- File -> Import ->Labels: `ann_quant.txt`
- File -> Import ->Audio: `quant_click.wav`
- Labels are annotated as `b` beat or `db` downbeat
- Labels that were automatically detected to have some problems are annotated with `W` after the name.

To export labels: File -> Export -> Labels : `ann_quant_cleaned.txt`

Test it, but don't work on it yet, because I need to figure out why it doesn't work for some authors.

### Notes Philippe

I understand that `midi_cleaned.mid` is a midi file produced from the score 
and I assume that the audio file has been generated from the same source.

It is unclear how the alignment file `ann_quant.txt` has been produced. There is the mention
of a "performed midi" and "score midi". Which text file is it? Also there are
two text files mentioned above. I am a bit lost.

Overall it seems that we do not annotate a true performance but a generated MIDI.


