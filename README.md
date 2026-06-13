
# OpenAssistant

An open-source AI administrative assistant that helps organize your daily work through intelligent morning briefings powered by Claude by Anthropic.

## Features

- **Morning Briefings**: Get a personalized summary of your day ahead
- **AI-Powered Organization**: Leverages Anthropic Claude Sonnet 4.6 for intelligent task analysis

This is mostly a fun project because I am just in a lot of positions and was struggling to keep up with my organization tools.
What this does is simple: it takes everything and creates a morning briefing out of it. First of all, it is designed as a cron job, meant to run on a Raspberry Pi or some other small server. 
It retrieves data from the following services:
- **Slack**
- **Outlook**
- **Gmail**
- **Google Sheets**
- **Google Calendar**
- **Outlook Calendar**
- **Todoist**
- **Github**
- **GeoIP**
- **Apple Health**
- **Plaid**

Feel free to add or remove services as you see fit, this is just the technology stack that I use, which makes it convenient for me to get a morning brief daily, with it fully organized. 

The Claude API then analyzes what is the prioritization by the provided prompt, and a temperature as low as possible without sounding entirely disjointed. 

It then auto-emails a draft every morning with everything that you need to look at.

## Getting Started

### Prerequisites

- Python 3.8+
- Claude API key

### Installation

Features are still being built. Hold for more information!

### Configuration

## Usage

## Cost
By brief analysis, it isn't that expensive with the design set forth here. It costs a max of 4-5 dollars per month, from API costs. But Claude isn't doing much more than some brief analysis using Sonnet 4.6, so it isn't chugging tokens than something that is a lot more AI-forward. In essence, it looks at all the data presented, which is textified into JSON and other machine-readable formats, so that Claude does nothing more than a quick browse over text, which inherently will consume less tokens. Furthermore, the number of agents running is kept to a minimum to ensure analysis is restricted. Furthermore, the temperature is kept low to minimize tokens as well.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

MIT License - see LICENSE file for details
