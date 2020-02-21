import pandas as pd
from pathlib import Path
import subprocess

MAESTRO_BPATH = Path("../datasets/maestro-v2.0.0/")  #you need to download the maestro dataset from https://magenta.tensorflow.org/datasets/maestro
VIRTUOSO_BPATH = Path("./")
NAK_PATH = Path("../nak_alignment")

df = pd.read_pickle("performance_dataframe_v2(bach).pkl")
align_perf = df[df["maestro_path"].notna()]


def delete_old_files(row):
    #delete the old alignment files
    Path(VIRTUOSO_BPATH,row["performed_midi_path"][:-5]+"_infer_corresp.txt").unlink()
    Path(VIRTUOSO_BPATH,row["performed_midi_path"][:-5]+"_infer_match.txt").unlink()
    Path(VIRTUOSO_BPATH,row["performed_midi_path"][:-5]+"_infer_spr.txt").unlink()

def generate_nak_align(row):
    subprocess.call(['python3', Path(NAK_PATH,"MIDIToMIDIAlign.sh"), row["score_midi_path"], row["performed_midi_path"]])

align_perf.apply(generate_nak_align)
align_perf