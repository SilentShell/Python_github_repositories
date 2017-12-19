import requests
import pandas
from bs4 import BeautifulSoup


def get_bestsellers(url, page_num):
    main_url = 'https://www.amazon.cn'
    seed_url = 'https://www.amazon.cn/gp/bestsellers/digital-text/116169071/ref=sa_menu_kindle_l3_116169071#{}'
    html = requests.get(url.format(page_num))
    html.encoding = 'utf-8'
    soup = BeautifulSoup(html.text, 'html.parser')
    raw = soup.find_all(class_='a-fixed-left-grid-inner')
    free_list = []
    paid_list = []
    for each in raw:
        book = {}
        book['rank'] = each.find_all(class_='zg_rankNumber')[0].text.strip('\n .')
        book['title'] = each.find_all(class_='p13n-sc-truncate p13n-sc-truncated-hyphen'
                                             ' p13n-sc-line-clamp-2')[0].text.strip()
        book['author'] = each.find_all(class_='a-size-small a-color-base')[0].text
        if each.find_all(class_='a-icon-alt'):
            book['star'] = each.find_all(class_='a-icon-alt')[0].text
        else:
            book['star'] = '无'
        book['price'] = each.find_all(class_='p13n-sc-price')[0].text
        book['url'] = main_url + each.find_all(class_='a-link-normal')[0]['href']
        print(book)
        if float(book['price'].strip('￥')) == 0:
            free_list.append(book)
        else:
            paid_list.append(book)
    return free_list, paid_list


if __name__ == '__main__':
    free_list = []
    paid_list = []
    seed_url1 = 'https://www.amazon.cn/gp/bestsellers/digital-text/116169071/ref' \
                '=zg_bs_116169071_pg_3?ie=UTF8&pg={}&ajax=1'
    seed_url2 = 'https://www.amazon.cn/gp/bestsellers/digital-text/116169071/ref' \
                '=zg_bs_116169071_pg_3?ie=UTF8&pg={}&ajax=1&isAboveTheFold=0'
    for page in range(1, 6):
        free_list += get_bestsellers(seed_url1, page)[0]
        paid_list += get_bestsellers(seed_url1, page)[1]
        free_list += get_bestsellers(seed_url2, page)[0]
        paid_list += get_bestsellers(seed_url2, page)[1]
    df1 = pandas.DataFrame(free_list)
    df1.to_excel('amazon_book_free_list.xlsx')
    df2 = pandas.DataFrame(paid_list)
    df2.to_excel('amazon_book_paid_list.xlsx')
