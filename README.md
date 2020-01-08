# Performed midi dataset


The dataset contains 1104 performances of 205 opus of classical piano, polyphonic music.

| Author       	| Performances 	| Opera 	|
|--------------	|--------------	|-------	|
| Bach         	| 172          	| 59    	|
| Balakirev    	| 10           	| 1     	|
| Beethoven    	| 279          	| 64    	|
| Brahms       	| 1            	| 1     	|
| Chopin       	| 296          	| 36    	|
| Debussy      	| 3            	| 2     	|
| Glinka       	| 2            	| 1     	|
| Haydn        	| 45           	| 12    	|
| Liszt        	| 122          	| 16    	|
| Mozart       	| 16           	| 3     	|
| Prokofiev    	| 8            	| 1     	|
| Rachmaninoff 	| 9            	| 5     	|
| Ravel        	| 36           	| 5     	|
| Schubert     	| 64           	| 15    	|
| Schumann     	| 28           	| 10    	|
| Scriabin     	| 13           	| 2     	|


#### Objectives

Build a dataset of classical piano, polyphonic MIDI performances, where each performance is associated to a:
- XML score files 
- MIDI score: a quantized MIDI file, similar to the XML score files, but in MIDI format and with the repetitions unravelled
- downbeats/beats position in the MIDI score
- downbeats/beats position in the MIDI performed
- alignments between each event in the MIDI performance and the corresponding event in the XML score 
- alignments between each event in the MIDI performance and the corresponding event in the MIDI score


#### Usage:
- ground truth for MIDI piano automatic music transcription (AMT) tasks
    - MIDI beat/downbeat tracking
    - MIDI quantization
    - voice separations
    - score structuring
- ground truth for piano expressive performance models
    

---
## Source Dataset
The dataset is obtained by curating the following dataset by Jeong et al.
(manual cleaning of the beat mark annotations)


- this dataset is used for the evalution of `VirtuosoNet` 
  https://github.com/jdasam/virtuosoNet
- the dataset is not public
- solo piano music, classical music, polyphonic, symbolic (MIDI + annote)

refs:


> Graph Neural Network for Music Score Data and Modeling Expressive Piano Performance
> Dasaem Jeong, Taegyun Kwon, Yoojin Kim, Juhan Nam 
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

The source dataset contains a set of performances from Yamaha competition (multiple performances of the same opus are present) named with the original name  `[performance].MID` (e.g.  `Zhdanov08.MID`). The following files are associated to each performance:
- XML score from musescore in musicXML format: `musicxml_cleaned.musicxml` 
- MIDI score (quantified MIDI) produced with Musescore from the musicXML file, duplicating the eventual repetitions in the score: `midi_cleaned.mid`
- automatic alignement (txt file)  between the performed midi and the score midi: `[performance]_infer_match.txt`
- automatic alignment (txt file) between the performed midi and the xml score: `[performance]_infer_corresp.txt`
  
The automatic alignment is produced with the following algoritm:
> Performance Error Detection and Post-Processing for Fast and Accurate Symbolic Music Alignment  
> Eita Nakamura, Kazuyoshi Yoshii, Haruhiro Katayose
> ISMIR 2017
> https://eita-nakamura.github.io/articles/EN_etal_ErrorDetectionAndRealignment_ISMIR2017.pdf

---
## Curation procedure

available at:  
https://github.com/fosfrancesco/performed-midi-dataset

In theory the automatic extraction of beats in the performance works in 2 steps:
1. we extract the beats from the MIDI score using the library PrettyMidi (better to start from the MIDI score than from the XML score because the repetitions are already unravelled),
2. from every beat in the MIDI score we compute a beat in the MIDI performance, using the automatic midi2midi alignment file.

In practise this automatic extraction presents the following problems:
- the beat in MIDI files (step 1) are not always computed correctly:
  - extra beats at the beginning
  - downbeats marked as beats and viceversa
  - extra downbeats in repetitions
  - misaligned beats (e.g. Ravel Pavane)
- the computation of the beat in the MIDI performance (step 2) may not be possible if:
  - there are no events happening at the beat position
  - the automatic alignment midi2midi is not correct because of player mistakes by
  - the automatic alignment midi2midi is not correct because the algotihm does not handle some situations (e.g.trillo )

So the idea is to **use the automatic extraction of beats and downbeats as a base and manually correct it**.

The new workflow is:
1. extract the beats/downbeats from the MIDI score using the library PrettyMidi (file `ann_quant.txt`)
2. manually correct the beats/downbeats of the MIDI score (file `ann_quant_cleaned.txt`)
   - Choose a Folder from the dataset (from authors above)
   - Open Audacity https://www.audacityteam.org/
   - File -> Import ->MIDI file: `midi_cleaned.mid`
   - File -> Import ->Labels: `ann_quant.txt`
      - Labels are annotated as `b` beat or `db` downbeat
      - Labels that were automatically detected to have some problems are annotated with `W` after the name.
   - File -> Import ->Audio: `quant_click.wav`
   - Manually correct the wrong labels
   - Export labels: File -> Export -> Labels : `ann_quant_cleaned.txt`
3. generate the beats/downbeats for the MIDI performances, using the corrected MIDI score annotations and the automatic midi2midi alignment (file `ann_unquant.txt`)
4. manually correct the beats/downbeats of the MIDI performance (file `ann_unquant_cleaned.txt`)

