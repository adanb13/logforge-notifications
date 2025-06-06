<div align="justify">
<p>
  <img align="left" src="https://raw.githubusercontent.com/rmfatemi/bitvoker/master/web/src/assets/bitvoker.svg" width="100" />
  <strong>bitvoker</strong> is an open-source, adaptable notification system engineered to optimize automated alerts from homelab environments to production infrastructures. It functions through a dedicated TCP server that ingests incoming messages. These messages can be refined into heavily customizable rule-based AI-generated summaries before being dispatched through various integrated destinations, including Slack, Discord, and Microsoft Teams.
</p>


## What Does It Do?

**bitvoker** transforms raw text and data into intelligent, actionable alerts. You send it the `log`/`text`/`website`, etc, and then configure it to do what you need. Leveraging regular expressions and AI, the following scenarios represent only a portion of its capabilities:

1. If logs coming from `web-app-gateway-03`, include `SECURITY_ALERT` and `Failed login attempt` for the user `admin` and the Client IP address is not within our internal `192.168.1.0/24` range, then use our local LLM model to identify the `origin of the attack` and `recommended blocking action`. Only send the AI-processed recommendations to the SOC team's `"INCIDENT" Slack channel` alerts. Never send the original security alerts (sensitive information).

2. If this downloaded BestBuy page contains a product-listing for `Sony WH-1000XM5 Headphones` then feed it into this AI model to see if the discount-badge shows a SAVE percentage greater than 15% and extracts the `current price`, `original price`, and the `direct buy URL`. Only send the AI-processed deal details to this dedicated `Telegram` chat.

3. If logs coming from the `db-server-prod-01` include an error where `long_query_threshold` exceeded and the duration is greater than `1000ms`, then use Meta's LLAMA4 model to summarize the `"impact on service in 15 words or less"`, send both the AI-processed summary and the original message, but the original message only if it contains a Client IP starting with `10.0.0..`. Send all notifications to the `DBA` team's `Microsoft Teams channel` and the team's `email alerts inbox`.


</div>

## Features

- 📢 **Multi-platform support**: **bitvoker** supports notifications for
  <p>
  <span>
    <img src="https://github.com/homarr-labs/dashboard-icons/blob/main/svg/telegram.svg" width="20">
    <img src="https://github.com/homarr-labs/dashboard-icons/blob/main/svg/slack.svg" width="20">
    <img src="https://github.com/homarr-labs/dashboard-icons/blob/main/svg/microsoft-teams.svg" width="20">
    <img src="https://github.com/homarr-labs/dashboard-icons/blob/main/svg/gmail.svg" width="20">
    <img src="https://github.com/homarr-labs/dashboard-icons/blob/main/svg/discord.svg" width="20">
    <img src="https://github.com/homarr-labs/dashboard-icons/blob/main/svg/whatsapp.svg" width="20">
    <img src="https://github.com/homarr-labs/dashboard-icons/blob/main/svg/gotify.svg" width="20">
    <img src="https://github.com/homarr-labs/dashboard-icons/blob/main/svg/ntfy.svg" width="20">
    <img src="https://github.com/homarr-labs/dashboard-icons/blob/main/svg/pushover.svg" width="20">
    <img src="https://github.com/homarr-labs/dashboard-icons/blob/main/svg/home-assistant.svg" width="20">
  </span>
   and many more thanks to Apprise integration.
</p>

- 🤖 **Customizable AI Processing**: Refine messages by summarizing them using customizable pre-prompts
- ☁️ **Cloud and Self-Hostable AI**: Use Meta’s LLAMA4 for cloud-based processing or Ollama for privacy
- 📜 **Notification History**: Store and browse past notifications with timestamps and source information
- 🖥️ **Web Dashboard**: Modern interface for configuration and notification management
- 🔄 **Real-time Updates**: Instantly receive notifications across all configured destinations
- ⚙️ **Dynamic Configuration**: Update settings without restarting the server
- 📊 **Detailed Logging**: Logging system accessible via web interface

## AI Processing

**bitvoker** offers AI-powered notification processing with fully customizable rules. This feature enables you to refine, summarize, and tailor notifications to your specific requirements by applying detailed matching conditions.

You can enable AI processing through unauthenticated interactions with [Meta's LLAMA4](https://www.meta.ai/) model or by self-hosting with [Ollama](https://ollama.com/). Define **pre-prompts** to dynamically guide AI behavior, and use the new rule system for granular control over how and when AI processing occurs.

---

### Flexible AI Processing Deployment

1.  **Meta's LLAMA4**:
    By default, **bitvoker** can connect to [Meta's LLAMA4](https://www.meta.ai/) model via unauthenticated API calls. This offers straightforward setup and immediate integration, though it is subject to API rate limits and regional availability.


>[!TIP]
> Users experiencing rate limits or availability issues with Meta’s service can either switch to Ollama or reduce/disable AI queries.



2.  **Self-Hosted Ollama**:
    **bitvoker** supports local AI processing with [Ollama](https://ollama.com/). Users prioritizing data privacy, stricter control, or seeking to bypass external usage limits are advised to opt for the self-hosted Ollama configuration. We recommend deploying a compact yet powerful model like `gemma3:1b` for optimal performance, even on systems with limited hardware.

---

### Customizable Notification Rule System

**bitvoker**'s rule system provides complete control over notification processing and delivery:
* **Dynamic Notification Delivery**: Complete control over notification destinations, including when, where, and what to send
* **Customizable Behavior**: Define rules to cutomize alerts based on source of alert, original content, AI prcessed content and more
* **Granular Control**: Maintain full control over sources, destinations, and AI behavior while preserving adaptable automation workflows

For a complete guide on how to define and use rules, refer to bitvoker's [wiki page](https://github.com/rmfatemi/bitvoker/wiki). Rules are defined in `YAML` format. You can use the provided reference to customize your own rule.

> [!TIP]
> If you are not comfortable working with `YAML` and regular expressions, any decent AI model can help you create your rules if you provide it with the reference and your requirements.
---

## 🏗️ Setup
This repository supports two ways of running **bitvoker**. For a consistent and isolated environment, using Docker is recommended.

### Docker

Create a `docker-compose.yaml` file copy the following inside it:

```yaml
services:
  bitvoker:
    image: ghcr.io/rmfatemi/bitvoker:latest
    container_name: bitvoker
    # --- Network Configuration ---
    # it is recommended to use host mode (refer to wiki for why)
    network_mode: host
    # for bridge mode comment the line above and uncomment ports
    # ports:
    #   - "8083:8083" # TCP server
    #   - "8084:8084" # TLS server
    #   - "8085:8085" # Web UI
    volumes:
      - logforge_notification_data:/app/data
      - /etc/localtime:/etc/localtime:ro
    restart: unless-stopped

volumes:
  logforge_notification_data:
    name: logforge_notification_data
```
Then start the service with:
```
docker-compose up -d
```
### Standalone Installation
#### Prerequisites

- Python 3.11 or higher
- [Poetry](https://python-poetry.org/docs/#installation) package manager
- [GNU Make](https://www.gnu.org/software/make/) utility
  -    `sudo apt-get install make` (Debian-based Linux), or `brew install make` (macOS)
1. Clone the repository:
    ```bash
    git clone https://github.com/rmfatemi/bitvoker.git
    cd bitvoker
    ```

2. Install dependencies:
    ```bash
    make install
    ```

3. Run the application:
    ```bash
    poetry run bitvoker
    ```

## 📝 Usage

You can send messages to **bitvoker**'s endpoint using `netcat` (port `8083`) for plaintext delivery, `openssl` (port `8084`) for secure connections, or by integrating it directly into your code via a `TCP socket`.

#### Plain text connection with netcat

`echo "Your notification message" | nc {server_ip} 8083`

#### Secure TLS connection with openssl

`cat {your_server_logs}.log | openssl s_client -connect {server_ip}:8084`

#### Plain text using a shell script
  ```shell
  #!/bin/bash
  echo "Your notification message" | nc {server_ip} 8083

  ```

#### Secure connection using in a Python script
  ```python
  import socket, ssl

  server_ip = "{server_ip}"
  port = 8084
  message = "Your notification message"

  context = ssl.create_default_context()

  with socket.create_connection((server_ip, port)) as sock:
      with context.wrap_socket(sock, server_hostname=server_ip) as s:
          s.sendall(message.encode())
  ```



### Web Interface
Access the web interface at `https://{server_ip}:8085` to:
- Configure notification destinations
- Adjust rules and AI settings
- View notification history
- View system logs

### Screenshots
<img src="https://github.com/user-attachments/assets/368f4842-59dd-4c38-a91d-a4478ca3efdb">
<img src="https://github.com/user-attachments/assets/04040c01-77bb-4bfd-9fa5-bf4c489f22ca">
<img src="https://github.com/user-attachments/assets/e3b79e6b-3482-411f-9179-fde5c0587227">
<img src="https://github.com/user-attachments/assets/ced0b8ae-25cd-4d51-addd-ba38f7b65e1a">

## 🔑 License

This project is licensed under the MIT License - see the [LICENSE]() file for details.
