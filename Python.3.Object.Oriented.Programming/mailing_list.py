from collections import defaultdict
import smtplib
from email.mime.text import MIMEText

def send_email(subject, message, from_addr, *to_addrs,
        host="localhost", port=1025, headers=None):
    """Send email.
    @param  subject   subject of the mail
    @param  message   contents of the mail
    @param  from_addr email address that the mail was sent from
    @param  to_addrs  variable length of addresses the mail was sent to
    @param  host      the smtp server
    @param  port      the port for the smtp server
    @param  headers   other attributes of the mail
    """
    headers = {} if headers is None else headers
    email = MIMEText(message)
    email["Subject"] = subject
    email["From"] = from_addr
    for header, value in headers.items():
        email[header] = value

    sender = smtplib.SMTP(host, port)
    for addr in to_addrs:
        del email["To"] # WARNING: DONT FORGET TO INCLUDE THIS LINE
        email["To"] = addr
        sender.sendmail(from_addr, addr, email.as_string())
    sender.quit()

class MailingList:
    """Manage groups of email addresses for sending emails."""
    def __init__(self):
        self.email_map = defaultdict(set)

    def add_to_group(self, email, group):
        """Add <email> address into one mailing <group>"""
        self.email_map[email].add(group)

    def emails_in_groups(self, *groups):
        """Return all emails in belonging to mailing <groups>."""
        groups = set(groups)
        return {e for (e, gs) in self.email_map.items() if gs & groups}

    def send_mailing(self, subject, message, from_addr,
                *groups, headers=None):
        """send email with <subject> and contents <message>  from <from_addr>
        to mailing <groups>."""
        emails = self.emails_in_groups(*groups)
        send_email(subject, message, from_addr, *emails, headers=headers)

