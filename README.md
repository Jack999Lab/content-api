\# AI Content Generator API



একটি সহজ AI কন্টেন্ট জেনারেটর API যা PHP ওয়েবসাইট থেকে কল করা যাবে।



\## Deploy করুন ফ্রিতে:



\### 1. Replit-এ Deploy

1\. Replit.com এ একাউন্ট করুন

2\. New Repl তৈরি করুন (Python)

3\. সব ফাইল আপলোড করুন

4\. Run বাটনে ক্লিক করুন

5\. আপনার API URL পেয়ে যাবেন: `https://your-project.repl.co`



\### 2. Railway.app-এ Deploy

1\. Railway.app এ GitHub কানেক্ট করুন

2\. এই রিপো select করুন

3\. Automatically deploy হবে

4\. URL: `https://your-project.up.railway.app`



\### 3. Render.com-এ Deploy

1\. Render.com এ নতুন Web Service তৈরি করুন

2\. GitHub কানেক্ট করুন

3\. Build Command: `pip install -r requirements.txt`

4\. Start Command: `python api.py`

5\. URL: `https://your-project.onrender.com`



\## API ব্যবহার:



```php

// PHP থেকে কল করুন

$url = "https://your-api-url/generate";

$data = \[

&nbsp;   'topic' => 'Artificial Intelligence',

&nbsp;   'keywords' => 'ai, machine learning',

&nbsp;   'tone' => 'professional',

&nbsp;   'length' => 500

];



// cURL ব্যবহার করুন

$ch = curl\_init($url);

curl\_setopt($ch, CURLOPT\_RETURNTRANSFER, true);

curl\_setopt($ch, CURLOPT\_POST, true);

curl\_setopt($ch, CURLOPT\_POSTFIELDS, json\_encode($data));

curl\_setopt($ch, CURLOPT\_HTTPHEADER, \['Content-Type: application/json']);



$response = curl\_exec($ch);

$result = json\_decode($response, true);

