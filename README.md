# captcha-service
A Web Service use OCR to figure captcha number from image

# python version
python3.6.8 - 64bit

# project installation
py -3 -m venv venv
venv\Scripts\activate
pip install Flask

# run project
venv\Scripts\activate
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run

# other
(venv) pip install ipykernel
(venv) pip install Pillow
(venv) pip install vietocr
(venv) pip install torch==1.7.1+cpu torchvision==0.8.2+cpu torchaudio===0.7.2 -f https://download.pytorch.org/whl/torch_stable.html
(venv) pip install pyyaml