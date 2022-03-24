# 画像ファイルを読み込んでNumpy形式に変換
import numpy as np
from PIL import Image
import os, glob, random

outfile = "image/photos.npz"    # 保存ファイル名
max_photo = 10                 # 利用する写真の枚数
photo_size = 32                 # 画像サイズ
x = []      # 画像データ
y = []      # ラベルデータ

def main():
    # 各画像のフォルダーを読む
    glob_files("./image/sushi", 0)
    glob_files("./image/salad", 1)
    # glob_files("./image/mabotofu", 2)
    glob_files("./image/soba", 3)
    glob_files("./image/okonomiyaki", 4)
    glob_files("./image/stake", 5)
    glob_files("./image/carry_and_rice", 6)
    glob_files("./image/gyoza", 7)
    
    """
    glob_files("./image/pizza", 8)
    glob_files("./image/omuraisu", 9)
    glob_files("./image/hamburger_stake", 10)
    glob_files("./image/doughnut", 11)
    glob_files("./image/shortcake", 12)
    glob_files("./image/parfait", 13)
    glob_files("./image/spring roll", 14)
    glob_files("./image/omlet", 15)
    glob_files("./image/natto", 16)
    glob_files("./image/miso_soup", 17)
    glob_files("./image/purin", 18)
    glob_files("./image/takoyaki", 19)
    glob_files("./image/chicken_namban", 20)
    glob_files("./image/hiyayakko", 21)
    glob_files("./image/toast", 22)
    glob_files("./image/rice", 23)
    glob_files("./image/grilled_fish", 24)
    glob_files("./image/apple", 25)
    glob_files("./image/tomato", 26)
    glob_files("./image/ahijillo", 27)
    glob_files("./image/medamayaki", 28)
    glob_files("./image/broccoli", 29)
    """
    # ファイルへ保存
    np.savez(outfile, x=x, y=y)
    print("保存しました:" + outfile, len(x))


# path以下の画像を読み込む
def glob_files(path, label):
    files = glob.glob(path + "/*.jpg")
    random.shuffle(files)
    # 各ファイルを処理
    num = 0
    for f in files:
        if num >= max_photo: break
        num += 1
        # 画像ファイルを読む
        img = Image.open(f)
        img = img.convert("RGB")                    # 色空間をRGBに
        img = img.resize((photo_size, photo_size))  # サイズ変更
        img = np.asarray(img)
        x.append(img)
        y.append(label)


if __name__ == "__main__":
    main()
