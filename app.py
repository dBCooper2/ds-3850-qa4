import os
from os.path import join, dirname
from dotenv import load_dotenv
from openai import OpenAI
from newsapi.newsapi_client import NewsApiClient
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

# Load environment variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

class NewsletterGenerator:
    def __init__(self):
        # Initialize NewsAPI and OpenAI
        self.newsapi = NewsApiClient(api_key=os.getenv('NEWS_API_KEY'))
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Email configuration
        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = int(os.getenv('SMTP_PORT'))
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')
        self.recipient_email = os.getenv('RECIPIENT_EMAIL')

    def fetch_news(self, topics, num_articles=5):
        """
        Fetch news articles for specified topics
        
        :param topics: List of news topics to search
        :param num_articles: Number of articles to retrieve
        :return: List of news articles
        """
        all_articles = []
        
        # Calculate date for fetching recent news (last 1 days)
        from_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        for topic in topics:
            try:
                # Fetch top headlines
                articles = self.newsapi.get_everything(
                    q=topic,
                    from_param=from_date,
                    language='en',
                    sort_by='publishedAt',
                    page_size=num_articles
                )
                
                all_articles.extend(articles['articles'])
            except Exception as e:
                print(f"Error fetching news for {topic}: {e}")
        
        return all_articles

    def summarize_article(self, article):
        """
        Use OpenAI to generate a concise summary of the article
        
        :param article: Article dictionary from NewsAPI
        :return: Summarized text
        """
        try:
            # Truncate article content if too long
            content = article['description'] or article['content'] or ''
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes news articles concisely."},
                    {"role": "user", "content": f"Summarize this news article in 3-4 sentences:\n\nTitle: {article['title']}\n\nContent: {content[:1000]}"}
                ],
                max_tokens=150
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error summarizing article: {e}")
            return f"Summary unavailable. Original title: {article['title']}"

    def create_newsletter(self, topics):
        """
        Create a newsletter by fetching and summarizing news
        
        :param topics: List of news topics
        :return: Formatted newsletter content
        """
        # Fetch articles
        articles = self.fetch_news(topics)
        
        # Generate newsletter content
        newsletter_content = "🗞️ Your AI Daily News Briefing 🗞️\n\n"
        newsletter_content += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        
        for article in articles[:5]:  # Limit to 10 articles
            summary = self.summarize_article(article)
            newsletter_content += f"📰 {article['title']}\n{summary}\n\n"
        
        return newsletter_content

    def send_email(self, newsletter_content):
        """
        Send newsletter via email
        
        :param newsletter_content: Formatted newsletter text
        """
        try:
            # Create message
            message = MIMEMultipart()
            message['From'] = self.sender_email
            message['To'] = self.recipient_email
            message['Subject'] = f"Daily News Briefing - {datetime.now().strftime('%Y-%m-%d')}"
            
            # Attach newsletter content
            message.attach(MIMEText(newsletter_content, 'plain'))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, self.recipient_email, message.as_string())
            
            print("Newsletter sent successfully!")
        except Exception as e:
            print(f"Error sending email: {e}")

def main():
    # Initialize newsletter generator
    generator = NewsletterGenerator()
    
    # Define topics of interest
    topics = ['technology', 'data science', 'programming', 'cybersecurity']
    
    # Create and send newsletter
    newsletter_content = generator.create_newsletter(topics)
    generator.send_email(newsletter_content)

if __name__ == "__main__":
    main()