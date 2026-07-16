from pathlib import Path
import shutil
import kagglehub

HANDLE="arashnic/the-depression-dataset"
OUT=Path("data/kaggle_depression")

def main():
    src=Path(kagglehub.dataset_download(HANDLE))
    OUT.mkdir(parents=True,exist_ok=True)
    for p in src.rglob("*"):
        if p.is_file():
            d=OUT/p.relative_to(src); d.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(p,d)
    print(f"Copied dataset to {OUT.resolve()}")
    for p in sorted(OUT.rglob("*")):
        if p.is_file(): print(" -",p.relative_to(OUT))

if __name__=="__main__": main()
