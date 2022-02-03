import pdfplumber
import time

def pdf_parse():
    with pdfplumber.open(r'WEF_GGGR_2021.pdf') as pdf:
        with open('result.csv', 'w') as result:
            csv = 'country; GGGI2006rank; GGGI2006score; GGGI2021rank; GGGI2021score; EPAO2006rank; EPAO2006score; EPAO2021rank; EPAO2021score; EA2006rank; EA2006score; EA2021rank; EA2021score; HAS2006rank; HAS2006score; HAS2021rank; HAS2021score; PE2006rank; PE2006score; PE2021rank; PE2021score'
            result.write(csv)
            page_number = 90
            while page_number < 401:
                pdf_pages = pdf.pages[page_number]
                page = pdf_pages.extract_text()
                if page.find('Bosnia') != -1:
                    country = '\nBosnia and Herzegovina'
                elif page.find('Congo, Democratic rank') != -1:
                    country = '\nCongo, Democratic Rep.'
                else:
                    country = page[(page.find('156 countries') + 13):((page.find('score ')) - 1)]
                page_new = page[((page.find('Economy')) + 8):(page.find('n\nHealth'))]
                page_list = page_new.replace('E ', '').replace('s d\n', '').replace('Politic ucatio ', '').replace('\n', ' ').split(' ')
                result.write(f'{country}; {page_list[4]}; {page_list[5]}; {page_list[6]}; {page_list[7]}; {page_list[12]}; {page_list[13]}; {page_list[14]}; {page_list[15]}; {page_list[18]}; {page_list[19]}; {page_list[20]}; {page_list[21]}; {page_list[25]}; {page_list[26]}; {page_list[27]}; {page_list[28]}; {page_list[31]}; {page_list[32]}; {page_list[33]}; {page_list[34]}')
                print(page_number)
                page_number += 2


if __name__ == '__main__':
    start_time = time.time()
    pdf_parse()
    print("--- %s seconds ---" % (time.time() - start_time))

