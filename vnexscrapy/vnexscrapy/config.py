DB_CONFIG = {
    'database': 'vnexpress',
    'user': 'postgres',
    'password': '30052002',
    'host': 'localhost',
    'port': '5432',
}

CRAWL_SETTINGS = {
    # 'DOWNLOAD_DELAY': 4,
    # 'CONCURRENT_REQUESTS': 5,
}

DOMAIN_CONFIG = [
    {
        'id': '1',
        'domain': 'vnexpress.net',
        'news_id_selector': 'head meta[name=tt_article_id]::attr(content)',
        'news_from_list_selector': '#automation_TV0 > div > .item-news > .title-news > a::attr(href)',
        'news_title_selector': 'head title::text',
        'publish_date_selector': 'head meta[name=pubdate]::attr(content)',
        'last_mod_selector': 'head meta[name=lastmod]::attr(content)',
        'author_selector': '.fck_detail p.Normal:last-of-type strong::text, .fck_detail p.author_mail strong::text',
        'description_selector': 'head meta[name=description]::attr(content)',
        'content_html_selector': '.container article.fck_detail',
        'content_text_selector': '.container article.fck_detail *::text',
        'keywords_selector': 'head meta[name=keywords]::attr(content)',
        'category_id_selector': 'head meta[name=tt_category_id]::attr(content)',
        'category_url_list_selector': '.ul-nav-folder li a::attr(href)',
        'category_title_selector': 'head meta[name=tt_list_folder_name]::attr(content)',
        'next_page_selector': 'a.btn-page.next-page::attr(href)'
    },
]
