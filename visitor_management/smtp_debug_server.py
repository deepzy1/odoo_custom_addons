import asyncio
import quopri
from aiosmtpd.controller import Controller
from email.parser import BytesParser
from email.policy import default


class CustomSMTPHandler:
    async def handle_DATA(self, server, session, envelope):
        # Decode the email data
        data = envelope.content
        message = BytesParser(policy=default).parsebytes(data)

        # Prepare message content
        output_content = ["---------- MESSAGE FOLLOWS ----------\n"]

        # Process each part of the message if it is multipart, or the whole message if it's single-part
        if message.is_multipart():
            for part in message.iter_parts():
                content_type = part.get_content_type()
                content_transfer_encoding = part.get("Content-Transfer-Encoding", "").lower()
                part_content = part.get_payload(decode=True) or b""

                # Decode quoted-printable content, handling errors
                if content_transfer_encoding == "quoted-printable":
                    try:
                        decoded_content = quopri.decodestring(part_content).decode("utf-8")
                    except UnicodeDecodeError:
                        # If decoding fails, fallback to binary content
                        decoded_content = part_content.decode("latin1", errors="replace")
                else:
                    try:
                        decoded_content = part_content.decode("utf-8", errors="replace")
                    except UnicodeDecodeError:
                        decoded_content = part_content.decode("latin1", errors="replace")

                output_content.append(f"Content-Type: {content_type}\n")
                output_content.append(decoded_content)
                output_content.append("\n")
        else:
            # Single-part message
            content_type = message.get_content_type()
            content_transfer_encoding = message.get("Content-Transfer-Encoding", "").lower()
            message_content = message.get_payload(decode=True) or b""

            if content_transfer_encoding == "quoted-printable":
                try:
                    decoded_content = quopri.decodestring(message_content).decode("utf-8")
                except UnicodeDecodeError:
                    decoded_content = message_content.decode("latin1", errors="replace")
            else:
                try:
                    decoded_content = message_content.decode("utf-8", errors="replace")
                except UnicodeDecodeError:
                    decoded_content = message_content.decode("latin1", errors="replace")

            output_content.append(f"Content-Type: {content_type}\n")
            output_content.append(decoded_content)
            output_content.append("\n")

        output_content.append("------------ END MESSAGE ------------\n\n")

        # Overwrite the email message to a file
        with open("emails_received.log", "w") as f:
            f.writelines(output_content)

        print("Email written to emails_received.log")
        return '250 Message accepted for delivery'


async def run():
    # Create the SMTP controller with the custom handler
    handler = CustomSMTPHandler()
    controller = Controller(handler, hostname='localhost', port=1025)
    controller.start()

    try:
        print("Custom SMTP Debugging Server running on localhost:1025")
        await asyncio.Event().wait()  # Keep the server running
    except KeyboardInterrupt:
        print("SMTP Debugging Server stopped.")
        controller.stop()


# Run the server
if __name__ == "__main__":
    asyncio.run(run())