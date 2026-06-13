
# OpenAssistant

An open-source AI administrative assistant that helps organize your daily work through intelligent morning briefings powered by Google Gemini.

## Features

- **Morning Briefings**: Get a personalized summary of your day ahead
- **AI-Powered Organization**: Leverages Anthropic Claude Sonnet 4.6 for intelligent task analysis

This is mostly a fun project because I am just in a lot of positions and was struggling to keep up with my organization tools.
What this does is simple: it takes everything and creates a morning briefing out of it. First of all, it is designed as a cron job, meant to run on a Raspberry Pi or some other small server. 
It retrieves data from the following services:
- **Slack**
- **Brightspace**
- **Outlook**
- **Gmail**
- **Google Sheets**
- **Google Calendar**
- **Outlook Calendar**
- **Facebook Messenger**
- **Todoist**
- **Github**
- **GeoIP**
- **Apple Health**
- **Plaid**

Feel free to add or remove services as you see fit, this is just the technology stack that I use, which makes it convenient for me to get a morning brief daily, with it fully organized. 

Google Gemini via OpenClaw then analyzes what is the prioritization by the provided prompt, and a temperature as low as possible without sounding entirely disjointed. 

It then auto-emails a draft every morning with everything that you need to look at.

## Getting Started

### Prerequisites

- Python 3.8+
- Google Gemini API key

### Installation

Features are still being built. Hold for more information!

### Configuration

## Usage

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

MIT License - see LICENSE file for details
