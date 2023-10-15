import subprocess

def start():
    try:
        # Define the Scrapy commands to run the two spiders
        db_init_cmd = ''
        category_spider_cmd = 'scrapy crawl category_spider'
        news_spider_cmd = 'scrapy crawl news_spider'

        subprocess.run(db_init_cmd, shell=True, check=True)
        subprocess.run(category_spider_cmd, shell=True, check=True)
        subprocess.run(news_spider_cmd, shell=True, check=True)

    except subprocess.CalledProcessError as error:
        print(f"Error: {error}")

if __name__ == "__main__":
    start()
