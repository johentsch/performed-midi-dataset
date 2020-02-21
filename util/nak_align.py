import pandas as pd
from pathlib import Path
import subprocess

MAESTRO_BPATH = Path("../datasets/maestro-v2.0.0/")  #you need to download the maestro dataset from https://magenta.tensorflow.org/datasets/maestro
VIRTUOSO_BPATH = Path("./")
NAK_PATH = Path("./util/nak_alignment")
NAK2DS_PATH = Path("../../")

df = pd.read_pickle("performance_dataframe_v2(bach).pkl")
align_perf = df[df["maestro_path"].notna()]


def delete_old_files(row):
    #delete the old alignment files
    Path(VIRTUOSO_BPATH,row["performed_midi_path"][:-5]+"_infer_corresp.txt").unlink()
    Path(VIRTUOSO_BPATH,row["performed_midi_path"][:-5]+"_infer_match.txt").unlink()
    Path(VIRTUOSO_BPATH,row["performed_midi_path"][:-5]+"_infer_spr.txt").unlink()

def generate_nak_align(row):
    subprocess.call([Path(NAK_PATH,"MIDIToMIDIAlign.sh"), Path(VIRTUOSO_BPATH,row["score_midi_path"][:-4]), Path(row["performed_midi_path"][:-4])])

def update_corresp_path(row):
    if pd.isnull(row["maestro_path"]):
        return row["midi2midi_alignment_path"]
    else:
        return row["midi2midi_alignment_path"].replace("_infer_corresp.txt","M_corresp.txt")



print("Creating ..................")
align_perf.apply(generate_nak_align,axis = 1)
print("Deleting old files ......................")
align_perf.apply(delete_old_files,axis = 1)
print("Updating the corresp ................")
df["midi2midi_alignment_path"] =df.apply(update_corresp_path,axis = 1) 

#save the new dataframe
df.to_pickle("performance_dataframe_v2(bach).pkl")