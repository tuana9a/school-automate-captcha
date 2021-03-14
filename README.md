# school-automate-captcha

A Web Service use OCR to figure number from HUST's Captcha

# python version

python3.6.8 - 64bit

# project installation (WINDOW)

py -3 -m venv venv
venv\Scripts\activate

# run project (WINDOW)

venv\Scripts\activate
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run

# packages (venv)

pip install Flask
pip install ipykernel
pip install Pillow
pip install vietocr
pip install torch==1.7.1+cpu torchvision==0.8.2+cpu torchaudio===0.7.2 -f https://download.pytorch.org/whl/torch_stable.html
pip install pyyaml
