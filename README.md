# Smart Assistant AI🤖

Smart Assistant AI is a cross-platform assistant project with both a native macOS desktop application and an interactive browser-based web edition.

The project began as a Python desktop assistant and has expanded into a Progressive Web App with persistent conversations, voice features, public API integrations, local AI, file analysis, chart generation, customizable themes, and privacy-friendly analytics.

## Live Web Application🌐

Open the interactive GitHub Pages version:

**Smart Assistant AI Web Edition**
https://jd-dev-king.github.io/SmartAssistantAI/

## GitHub Repository

https://github.com/jd-dev-king/SmartAssistantAI

---

## Project Overview

Smart Assistant AI demonstrates practical experience with:

* Python desktop application development
* JavaScript web application development
* Local and browser-based AI
* REST API integrations
* Progressive Web Apps
* Browser storage and state management
* Speech recognition and text-to-speech
* Data visualization
* CSV and JSON analysis
* Responsive user interface design
* macOS application packaging
* Git and GitHub deployment

The project contains two primary editions.

### Desktop Edition

The native macOS desktop application is built with Python and Tkinter.

It includes:

* Conversational assistant interface
* Persistent JSON-based memory
* User profile recognition
* Calculator
* Dictionary lookup
* Wikipedia summaries
* Jokes
* System monitoring
* CPU and memory status
* Battery status
* Local file search
* Native application launcher
* Voice output
* Chat history
* Export functionality
* Packaged macOS `.app`

### Web Edition

The browser-based edition is built with HTML, CSS, and JavaScript and is hosted through GitHub Pages.

It includes:

* Interactive browser-based assistant
* Built-in Tools mode
* Optional Local AI mode
* Persistent browser memory
* Multiple saved conversations
* Conversation search
* Voice input
* Text-to-speech
* Rich weather cards
* Rich dictionary cards
* Rich Wikipedia cards
* Calculator and percentage calculations
* Current date and time
* Jokes
* CSV and JSON file upload
* Local data preview
* Automatic numeric-column detection
* Bar charts
* Line charts
* Pie charts
* Scatter charts
* Chart PNG downloads
* Local usage analytics dashboard
* Chat and analytics export
* Progressive Web App installation
* Offline application shell
* Responsive desktop and mobile layouts
* Eight appearance modes

---

## Assistant Modes

### Built-in Tools

Built-in Tools are available immediately and do not require an AI model.

Supported tools include:

* Weather
* Calculator
* Percentage calculations
* Dictionary
* Wikipedia
* User memory
* Jokes
* Date and time
* File analysis
* Chart generation
* Voice tools

### Local AI

Local AI uses WebLLM to run an open-source language model directly inside a compatible browser.

Local AI provides:

* Open-ended questions
* General explanations
* Contextual follow-up responses
* Private in-browser inference
* Conversation context
* Saved profile context

The model must be loaded before Local AI can be used. The first load may require a large model download.

A recent WebGPU-compatible version of Chrome or Edge is recommended.

### Cloud AI

Cloud AI is planned for a future release.

A secure backend is required before a hosted AI provider can be integrated because API keys must not be stored in public GitHub Pages JavaScript.

---

## Rich Response Cards

The Web Edition displays structured cards for supported API responses.

### Weather Cards

Weather cards include:

* City and state
* Current temperature
* Feels-like temperature
* Humidity
* Wind speed
* Current conditions

Example commands:

```text
weather Philadelphia, PA
what is the weather in Fort Washington, PA?
what's the weather in New York, NY?
how is the weather in Atlanta, Georgia?
```

### Dictionary Cards

Dictionary cards include:

* Word
* Part of speech
* Definition
* Usage example when available
* Source link when available

Example:

```text
define automation
```

### Wikipedia Cards

Wikipedia cards include:

* Article title
* Description
* Summary
* Thumbnail image when available
* Link to the complete article

Example:

```text
wiki Nikola Tesla
```

---

## Persistent Memory

The assistant can remember selected user information.

Examples:

```text
my name is Jeremiah
my favorite color is blue
i work as a process engineer
```

The assistant can later recall the saved information:

```text
what is my name
what is my favorite color
what is my job
```

Desktop memory is stored in JSON files.

Web Edition memory is stored in browser `localStorage`.

---

## Multiple Conversations

The Web Edition supports multiple saved conversations.

Users can:

* Start a new conversation
* Switch between conversations
* Rename conversations
* Delete conversations
* Search the active conversation
* Export the active conversation
* Retain conversations after refreshing the browser

Conversation history remains stored locally in the browser.

---

## Voice Features

### Voice Input

The microphone button uses browser speech recognition to convert spoken questions into text.

The browser may request microphone permission.

Voice recognition support varies by browser and may require an internet connection.

### Speech Output

The speaker button reads the assistant's latest response aloud using the browser Speech Synthesis API.

Automatic speech can also be enabled in Settings.

---

## Animated Assistant Avatar

The assistant avatar changes based on application activity.

Available states include:

* Idle
* Thinking
* Listening
* Speaking
* Loading Local AI

The avatar provides a visual indication of the assistant's current status.

---

## File Analyzer

The Web Edition includes a local CSV and JSON file analyzer.

Uploaded files remain inside the browser and are not sent to a server.

Supported formats:

```text
.csv
.json
```

The file analyzer provides:

* Row count
* Column count
* Numeric-column detection
* Missing-value count
* Data preview
* Chart field selection
* Chart generation
* PNG chart downloads
* Chart summary insertion into chat

### Example CSV

```csv
month,revenue,expenses
January,120000,80000
February,135000,85000
March,142000,91000
April,155000,94000
May,162000,98000
```

---

## Chart Generation

The file analyzer uses Chart.js.

Supported chart types:

* Bar
* Line
* Pie
* Scatter

Users can select:

* Chart type
* Label column
* Value column
* X-axis and Y-axis columns for scatter charts

Generated charts can be downloaded as PNG images.

---

## Local Analytics Dashboard

The analytics dashboard stores usage metrics only in the visitor's browser.

Tracked metrics include:

* Messages sent
* Assistant responses
* Conversations created
* Weather requests
* Dictionary requests
* Wikipedia searches
* Calculator usage
* Local AI prompts
* Voice input sessions
* Spoken responses
* Files analyzed
* Charts generated
* Charts downloaded
* Theme selections
* Chat exports

The dashboard includes:

* Headline metric cards
* Seven-day activity chart
* Most-used tools chart
* Assistant-mode usage
* Theme usage
* File and chart activity
* Voice activity
* JSON analytics export
* Reset analytics control

No analytics data is transmitted to an external server.

---

## Themes

The Web Edition includes eight appearance modes:

* Dark Blue
* Light
* Corporate
* Terminal
* Glass
* Cyberpunk
* Material
* System Default

The selected theme is saved in browser storage.

---

## Progressive Web App

The Web Edition is configured as a Progressive Web App.

Supported PWA features include:

* Web app manifest
* Service worker
* Offline application shell
* Installable standalone experience
* App icon
* Theme color
* Online and offline status
* Cached HTML, CSS, JavaScript, and local assets

Some tools still require an internet connection:

* Weather
* Dictionary
* Wikipedia
* Initial Local AI model download
* Speech recognition in some browsers

Local tools that can continue working offline include:

* Calculator
* Memory
* Saved conversations
* Conversation search
* Themes
* File analysis
* Charts
* Analytics
* Local jokes

---

## Technology Stack

### Desktop Edition

* Python
* Tkinter
* JSON
* PyInstaller
* psutil
* pyttsx3
* Public REST APIs

### Web Edition

* HTML5
* CSS3
* JavaScript ES modules
* WebLLM
* Chart.js
* Papa Parse
* Open-Meteo
* Dictionary API
* Wikipedia REST API
* Web Speech API
* Speech Synthesis API
* WebGPU
* Local Storage
* Service Workers
* Progressive Web App manifest
* GitHub Pages

---

## Project Structure

```text
SmartAssistantAI/
├── api/
│   ├── dictionary.py
│   ├── jokes.py
│   ├── weather.py
│   └── wiki.py
├── assets/
│   └── icon.icns
├── calculator/
├── gui/
├── memory/
├── system/
├── utilities/
├── voice/
├── docs/
│   ├── assets/
│   │   └── smart-ai-logo.png
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   ├── manifest.webmanifest
│   └── service-worker.js
├── main.py
├── chatbot.py
├── config.py
├── requirements.txt
├── Smart Assistant AI.spec
└── README.md
```

---

## Running the Desktop Edition

### 1. Clone the repository

```bash
git clone https://github.com/jd-dev-king/SmartAssistantAI.git
cd SmartAssistantAI
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the environment

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
python main.py
```

---

## Building the macOS Application

Activate the virtual environment and run:

```bash
pyinstaller --clean "Smart Assistant AI.spec"
```

The packaged application will be created in:

```text
dist/Smart Assistant AI.app
```

Desktop user data is stored in:

```text
~/Library/Application Support/SmartAssistantAI/
```

This includes:

```text
profile.json
history.json
```

---

## Running the Web Edition Locally

The Web Edition should be opened through an HTTP development server rather than directly as a `file://` page.

### Visual Studio Code Live Server

1. Open the repository in Visual Studio Code.
2. Open `docs/index.html`.
3. Right-click the file.
4. Select **Open with Live Server**.

### Python local server

From the repository root:

```bash
cd docs
python3 -m http.server 8000
```

Then open:

```text
http://localhost:8000
```

---

## Service Worker Updates

When deploying changes to the web application, update the cache name inside:

```text
docs/service-worker.js
```

Example:

```javascript
const CACHE_NAME =
    "smart-assistant-ai-v2-cache-5";
```

Increment the cache version when a previously installed cache must be replaced.

After updating the service worker:

1. Open browser Developer Tools.
2. Go to **Application**.
3. Select **Service Workers**.
4. Unregister the old worker.
5. Select **Storage**.
6. Clear site data.
7. Hard-refresh the page.

---

## Testing Commands

### Memory

```text
my name is Jeremiah
what is my name
my favorite color is blue
what is my favorite color
i work as a process engineer
what is my job
```

### Calculator

```text
calculate 125 * 8
solve (35 + 15) / 2
15 percent of 300
```

### Weather

```text
weather Philadelphia, PA
what is the weather in Fort Washington, PA?
```

### Dictionary

```text
define automation
```

### Wikipedia

```text
wiki Nikola Tesla
tell me about artificial intelligence
```

### Local AI

```text
Explain Lean Six Sigma in beginner-friendly terms.
How is it used in pharmaceutical manufacturing?
```

---

## Privacy

Smart Assistant AI is designed to keep most user data local.

The Web Edition stores the following in browser storage:

* User profile
* Conversations
* Settings
* Theme preference
* Analytics

CSV and JSON files are processed locally and are not uploaded to a server.

Local AI prompts are processed inside the browser when WebLLM mode is active.

Public API commands send only the information required for the request, such as a city name, dictionary word, or Wikipedia topic.

---

## Current Limitations

* Local AI requires WebGPU.
* The first Local AI model load may be large.
* Local AI performance depends on the visitor's device.
* Speech recognition availability depends on the browser.
* Weather, dictionary, and Wikipedia require internet access.
* Cloud AI is not yet implemented.
* Image generation is not yet implemented.
* PDF, DOCX, and XLSX parsing are planned for a later release.
* Browser storage is specific to the browser and device being used.

---

## Future Roadmap

Planned enhancements include:

* Secure Cloud AI backend
* Image generation
* PDF analysis
* DOCX analysis
* XLSX analysis
* Expanded chart recommendations
* Advanced file summaries
* Markdown rendering
* Additional response cards
* Optional account-based synchronization
* Expanded accessibility testing
* Automated web testing

---

## Version History

### Version 2.2.0 — Web Analytics and Data Tools

* Added CSV and JSON file analyzer
* Added bar, line, pie, and scatter charts
* Added PNG chart downloads
* Added local analytics dashboard
* Added analytics export
* Added rich API response cards
* Added animated assistant avatar
* Added Cyberpunk and Material themes
* Added clear Built-in Tools and Local AI modes

### Version 2.1.0 — Local AI and PWA

* Added Local AI through WebLLM
* Added Progressive Web App support
* Added service-worker caching
* Added offline application shell
* Added multiple themes
* Added voice input and output
* Added multiple conversations
* Added conversation search

### Version 1.0.0 — Desktop Edition

* Initial Python desktop assistant
* Persistent memory
* Voice output
* Calculator
* Dictionary
* Wikipedia
* Jokes
* Weather integration
* System monitoring
* File search
* Application launcher
* Packaged macOS application

---

## Author

**Jeremiah Lupton**

GitHub:
https://github.com/jd-dev-king

Portfolio:
https://jeremiahlupton.com

---

## License

This project is intended for educational, portfolio, and demonstration purposes.

Add a formal open-source license file before using or distributing the project under a specific license.

