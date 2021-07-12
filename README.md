# captcha-predict.automation.hust-assistant.com

from HUST's Captcha to number

# REQUIREMENTS

<strong><i style="color:red">CAUTION:</i> vietocr use pyyaml</strong>
- <code>pip install Flask==2.0.1</code>
- <code>pip install torch==1.7.1+cpu torchvision==0.8.2+cpu torchaudio===0.7.2 -f https://download.pytorch.org/whl/torch_stable.html</code>
- <code>pip install Pillow==8.2.0</code>
- <code>pip install pyyaml==5.4.1</code>
- <code>pip install vietocr==0.3.2</code>

# WINDOW

<strong><i style="color:red">CAUTION:</i> setup trên window dễ bị lỗi khi cài libs</strong>
<h2>setup</h2>

- <code>python3.6.8</code>
- <code>py -m venv venv</code>
- <code>venv\Scripts\activate</code>
<h2>run</h2>

- <code>venv\Scripts\activate</code>
- <code>python main.py</code>

# LINUX

<strong><i style="color:red">CAUTION:</i> có thể venv bị lỗi connection refused</strong>
<h2>setup</h2>

- <code>python3.9.5</code>
- <code>python -m venv venv</code>
- <code>source venv/bin/activate</code>
<h2>run</h2>

- <code>source venv/bin/activate</code>
- <code>python main.py</code>