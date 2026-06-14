
# OpenAssistant

An open-source AI administrative assistant that helps organize your daily work through intelligent morning briefings powered by Claude by Anthropic.

## Features

- **Morning Briefings**: Get a personalized summary of your day ahead
- **AI-Powered Organization**: Leverages Anthropic Claude Sonnet 4.6 for intelligent task analysis
- **Multi-model AI subagent organization**: Levarages Gemini Flash & Mistral to better present & analyze complex systems for improved token costs.

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

The Claude API then analyzes what is the prioritization by the provided prompt, and a temperature as low as possible without sounding entirely disjointed. Gemini and Mistral are assistants who help with some subtasks, which will be for a future update which will have more functionality than a pure morning briefing, but rather continuous AI support, akin to a smart assistant who can do everything from remind you about projects to helping you reorganize your meetings, and more. But that is in the future, but the baseboards are being built for it, so I am mentioning it  now.

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

## Contributing & Warnings 

Contributions are welcome! Please fork the repository and submit a pull request.

Keep in mind that I am not a professional software developer. I'm a bioinformatician and a college student. I am not an AI engineer, I do not work for Anthropic / OpenAI / AMI, and I do not have the engineering skill of someone who develops for those companies. I am a student & a *biology* researcher who happens to code. I am entirely incapable of guaranteeing that if you use this, it will work correctly. For what it's worth, I would love to fix any bugs or issues found, but I am making this on my own time and using my own money and compute. So, this is not a project that is meant for commercial use, and if you choose to use it for your daily life, you understand that it is at your own risk. AI agents are unpredictable, and as much as I have engineered the prompts to keep them from going off the rails, they still might.

There is also an existential risk in using technology like this. A morning briefing is pretty innocuous, but as more features are added, you may find that even a system that does not use something like Opus or Fable is still capable of a lot of things. Due to this, you might lose your own capacity to do these things. If you have to never deal with emails again, you may find that you lose the skill of dealing with emails, and may find it difficult to return to doing so if your system ever goes down. If you choose to let this system handle things like your iMessage (an API not provided here, but something that could be built), you might lose your capacity to chat with people. While **I AM NOT CLAIMING THIS SIMPLE PROJECT CAN DO ANY OF THAT**, I am illustrating a warning. Please do not rely on improving any technology like this to replace your own competency, but rather use it to improve the drudgery of life. Future builds of this system, as I engineer more features, will also have hard-coded gates to prevent misuse. While it is trivial to remove these gates, I strongly discourage it.

## License

MIT License - see LICENSE file for details






