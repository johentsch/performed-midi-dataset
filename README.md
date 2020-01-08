are associated to each performance:
> https://eita-nakamura.github.io/art> Eita Nakamura, Kazuyoshi Yoshii, Haruhiro Katayose
> ISMIR 2017
> https://eita-nakamura.github.io/articles/EN_etal_ErrorDetectionAndRealignment_ISMIR2017.pdf

---
## Curation procedure

available at:  
https://github.com/fosfrancesco/performed-midi-dataset

The> ISMIR 2017
> httpsg ateita-nakamuragithub.io/art> https://eita-nakamura.github.io/articles/EN_etal_ErrorDetectionAndRealignment_ISMIR2017.pdf

The source dataset contains a set of performances from Yamaha competition (multiple performances of the same opus are present). The following files are associated to each performance:
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
## Curation procedure

available at:  
https://github.com/fosfrancesco/performed-midi-dataset

The automatic extraction of beats in the performance works in 2 steps:
1. we extract the beats from the MIDI score using the library PrettyMidi,
2. from every beat in the MIDI score we compute a beat in the MIDI performance, using the automatic midi2midi alignment file.

This automatic extraction presents the following problems:
- the beat in MIDI files are not always computed correctly:
  - extra beats at the beginning
  - downbeats marked as beats and viceversa
  - extra downbeats in repetitions
  - misaligned beats (e.g. Ravel Pavane)
- the computation of the beat in the MIDI performance may not be possible if:
  - there are no events happening at the beat position
  - the automatic alignment midi2midi is not correct because of player mistakes by
  - the automatic alignment midi2midi is not correct because the algotihm does not handle some situations (e.g.trillo )

So the idea is to use the automatic extraction of beats and downbeats as a base and manually correct it.


The procedure is:
- Choose a Folder from the dataset (from authors above)
- Open Audacity https://www.audacityteam.org/
- File -> Import ->MIDI file: `midi_cleaned.mid`
- File -> Import ->Labels: `ann_quant.txt`
- File -> Import ->Audio: `quant_click.wav`
- Labels are annotated as `b` beat or `db` downbeat
- Labels that were automatically detected to have some problems are annotated with `W` after the name.

To export labels: File -> Export -> L---
ach         	| 172          	| 59    	|
|f sl>kirev    	| 10           	| 1     	|
| Beethoven    	| 279          	| 64    	|
> Brahms            	| 1     	|
| 17.>Chopin      MIDI score (quantified MIDI) produced with Musescore from  (qupdf

            	| 2     	|
| Glinka       	| 2             	| 1     	|
| Haydn  0a23101a093c554b00063191c2fe612174bdb1f7
- XML score from musescore in musicXMLcore tion procedu(quantified MIDI) produced with Musere
re fro       	| 45           	| 12    	|
| Liszt        	| 122          	| 16    	|
score  Mozart       	| 16           	| 3     	|
Rachmaninoff 	| 9 iith tned we, 
   duplicat rom the musicinthe XML fiile) between the performed midi and the score midi,
tain elo
- alit file) bgnment (t> Performance Error Det> Performance Errorignment (tigetween the performed midi and the xml score, 
  obtahe Nakamura algo    duplicating the- alignement (txt for Detbelow.
  
> Performance Err           	| 2     	|


## >bjectives

Build a dataset of classical piano, polyphonic MIDI performances, where each performance is associated to a:
- XML score files 
- MIDI score
- down-beat / beat annotations (dates in performance)
- alignments between each event in the MIDI performance and the corresponding event in the XML score
- alignments between each event in the MIDI performance and the corresponding event in the MIDI score


#### Usage:
- <<<<<<< HEAD
Theground truth for MIDI piano automatic music transcription (AMT) tasks
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
erformance Errorerformance Error Detection andPost-Processing for Fast and Accue Symbolic Music Alignment  
> Eita Nakamura, Kazuyorashi Yoshii, Haruiro Katayose
> ISMIR 27
> https://ei>> Graph Neural Networph NeuraliGraph Neural Nlable at:  
https:etwork for Music Score Data and Modeling Expressive Piano Performance
Dasaem

ava aJeong, Taegmuragithub.io/articles/EN_al_ngs oErrof the 36trDetect/github.com/fosfcesco/performed-mid-dataset

The Conference on Machine Learning, PMLR 97:3060-3070, 2019.
> http://proceedings.mlrh contains a set of performances froha competit.press/v97/jeong19a.html


> Virtm Atteion for Generatin 
(mugThe source dataset contains a set of performances from Yamaha competition (multiplee source datat contaiee dataset conf perfors from Yamaha competion 
(ns a set of performances from Yamaha competition (multiple performances of the same opus are present). The following files are associated to each performance:
=======
Tultiple performances ofhe sameA Hierarchical Attention RNN for Generating Expressive Piano Performance from Music Score
> Dasaem Jeong, Taegyun Kwon, Juhan Nam
> NIPS 2018
> https://github.com/jdasam/virtuosoNet

> VirtuosoNet: A Hierarchical RNN-based System for Modeling Expressive Piano Performance  
> Dasaem Jeong; Taegyun Kwon; Yoojin Kim; Kyogu Lee; Juhan Nam
> Mhives.ismir.net/ismir2019/paper/000112.pdf

The source dataset contains a set of performances from Yamaha competition (multiple performances of the same opus are present). The following files are associated to each performance:
(multiple performances of the same(multiple performances of the same opus are present). The following files 
matic extraction of beats in the performance works in 2 steps:
1. we extract the beats from the MIDI score using the library PrettyMidi,
2. from every beat in the MIDI score we compute a beat in the MIDI performance, using the automatic midi2midi alignment file.

This automatic extraction presents the following problems:
- the beat in MIDI files are not always computed correctly:
  - extra beats at the beginning
  - downbeats marked as beats and viceversa
  - extra downbeats in repetitions
e computation of the beat in the MIDI performance may not be possible if:
 alignment midi2midi is not correct because the algotihm does not handle some situations (e.g.trillo )

So the idea is to use the automatic extraction of beats and downbeats as a base and manually correct it. We first correct the beats/downbeats for the MIDI score and then we for the MIDI performances.

