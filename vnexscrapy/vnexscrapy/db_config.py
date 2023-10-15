db_config = {
    'database': 'vnexpress',
    'user': 'postgres',
    'password': '30052002',
    'host': 'localhost',
    'port': '5432',
}

domain_config = [
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

create_query_news = """
                        CREATE TABLE IF NOT EXISTS news (
                           id TEXT PRIMARY KEY,
                           title TEXT,
                           source_id TEXT REFERENCES source(id) ON DELETE CASCADE,
                           category_id TEXT REFERENCES category(id) ON DELETE SET NULL,
                           author TEXT,
                           description TEXT,
                           content_html TEXT,
                           content_text TEXT,
                           keywords TEXT
                        );
                        """

create_query_category = """
                        CREATE TABLE IF NOT EXISTS category (
                           id TEXT PRIMARY KEY,
                           title TEXT
                        );
                        """

create_query_source = """
                        CREATE TABLE IF NOT EXISTS source (
                           id TEXT PRIMARY KEY,
                           url TEXT,
                           domain TEXT,
                           title TEXT,
                           publish_date TEXT,
                           last_mod TEXT,
                           author TEXT
                        );
                        """

create_query_config = """
                        CREATE TABLE IF NOT EXISTS config (
                            id TEXT PRIMARY KEY,
                            domain TEXT,
                            news_id_selector TEXT,
                            news_from_list_selector TEXT,
                            news_title_selector TEXT,
                            publish_date_selector TEXT,
                            last_mod_selector TEXT,
                            author_selector TEXT,
                            description_selector TEXT,
                            content_html_selector TEXT,
                            content_text_selector TEXT,
                            keywords_selector TEXT,
                            category_id_selector TEXT,
                            category_url_list_selector TEXT,
                            category_title_selector TEXT,
                            next_page_selector TEXT
                        );
                        """
