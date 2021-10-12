import requests
from bs4 import BeautifulSoup
#11번가 API#
#apiCode에 따른 4가지 URL명령을 4함수로 구현        ##자세한 파라미터 설명은 아래에...
#상품 검색
def get_ProductSearch_page(apiCode0="ProductSearch",keyword="",pageNum=1,pageSize=50,Categories="",sortCd="",targetSearchPrd="KOR"):
    key="7849d05dcfe1093868e7cfc7ad29da4d"

    search_basic = f"http://openapi.11st.co.kr/openapi/OpenApiService.tmall?key={key}&apiCode={apiCode0}&keyword={keyword}"
    if pageNum !=1:
        search_basic=search_basic+f"&pageNum={pageNum}"
    if pageSize !=50:#최대 200
        search_basic=search_basic+f"&pageSize={pageSize}"
    if Categories !="":
        search_basic=search_basic+f"&option={Categories}"
    if sortCd !="":
        search_basic=search_basic+f"&sortCd={sortCd}"
    if targetSearchPrd !="KOR":
        search_basic=search_basic+f"&targetSearchPrd={targetSearchPrd}"
    
    page=requests.get(search_basic)
    xmlRow = page.content.decode('cp949')
    
    soup = BeautifulSoup(xmlRow,'html.parser')
    return soup,page,keyword,sortCd
#상품 상세
def get_ProductInfo_page(apiCode0="ProductInfo",productCode=1000,Categories=""):
    key="7849d05dcfe1093868e7cfc7ad29da4d"

    search_basic = f"http://openapi.11st.co.kr/openapi/OpenApiService.tmall?key={key}&apiCode={apiCode0}&productCode={productCode}"
    if Categories !="":
        search_basic=search_basic+f"&option={Categories}"
    
    page=requests.get(search_basic)
    xmlRow = page.content.decode('cp949')
    
    soup = BeautifulSoup(xmlRow,'html.parser')
    return soup,page
#카테고리정보(거의 무용지물인 api)                  ##안씀
def get_CategoryInfo_page(apiCode0="CategoryInfo",categoryCode=1,pageNum=1,pageSize=50,Categories="",sortCd=""):
    key="7849d05dcfe1093868e7cfc7ad29da4d"
    
    search_basic = f"http://openapi.11st.co.kr/openapi/OpenApiService.tmall?key={key}&apiCode={apiCode0}&categoryCode={categoryCode}"
    if pageNum !=1:
        search_basic=search_basic+f"&pageNum={pageNum}"
    if pageSize !=50:#최대 200
        search_basic=search_basic+f"&pageSize={pageSize}"
    if Categories !="":
        search_basic=search_basic+f"&option={Categories}"
    if sortCd !="":
        search_basic=search_basic+f"&sortCd={sortCd}"
    
    page=requests.get(search_basic)
    xmlRow = page.content.decode('cp949')
    
    soup = BeautifulSoup(xmlRow,'html.parser')
    return soup,page
#상품 이미지페이지(굳이 얘를 쓸필요는 없을것같다)     ##안씀
def get_ProductImage_page(apiCode0="ProductImage",categoryCode=1,productCode=1000):
    key="7849d05dcfe1093868e7cfc7ad29da4d"

    search_basic = f"http://openapi.11st.co.kr/openapi/OpenApiService.tmall?key={key}&apiCode={apiCode0}&categoryCode={categoryCode}&productCode={productCode}"

    page=requests.get(search_basic)
    xmlRow = page.content.decode('cp949')
    
    soup = BeautifulSoup(xmlRow,'html.parser')
    return soup,page

#최종 -----------------------------------------------------------------------------------------------------------------------------------------------------------
def get_page(apiCode="ProductSearch",**kargs):
    if apiCode == "ProductSearch":
        return get_ProductSearch_page(apiCode0=apiCode, **kargs)
    if apiCode == "ProductInfo":
        return get_ProductInfo_page(apiCode0=apiCode, **kargs)
    if apiCode == "CategoryInfo":                                       #실제로 사용하진않음(의미가없음)
        return get_CategoryInfo_page(apiCode0=apiCode, **kargs)
    if apiCode == "ProductImage":                                       #실제로 사용하진않음
        return get_ProductImage_page(apiCode0=apiCode, **kargs)

#주어진 dictionary에 json화시킬 데이터(soup) 삽입. 
def tojson_PS(func_get_page,Data_Origin={},start_num=0):
    num=start_num
    #json가장 첫 배열명은 검색키워드명
    keyword=func_get_page[2]
    title=keyword
    #sort입력시엔 뒤에 정령방식추가
    sortCd_value=func_get_page[3]
    
    if sortCd_value=="":
        pass
    elif sortCd_value=="CP":
        title=title +"_인기도순"
    elif sortCd_value=="A":
        title=title +"_누적판매순"
    elif sortCd_value=="G":
        title=title +"_평가높은순"
    elif sortCd_value=="I":
        title=title +"_후기와리뷰많은순"
    elif sortCd_value=="L":
        title=title +"_낮은가격순"
    elif sortCd_value=="H":
        title=title +"_높은가격순"
    elif sortCd_value=="N":
        title=title +"_최근등록순"
    else:
        pass
    
    if not(title in Data_Origin.keys()): 
        Data_Origin[title]={}

    
    #end값 구하기
    origin_soup=func_get_page[0]
    counts=len(origin_soup.find_all("product"))
    end_num=num+counts
    
    #데이터추출
    for product in origin_soup.find_all("product"):
        #데이터 값만 추출
        ProductCode=int(product.productcode.contents[0])
        #ProductInfo에 있는 값도 가져오기위해 ProductCode는 미리 추출
        PIsoup=get_page(apiCode="ProductInfo",productCode=ProductCode)[0]
        PI=PIsoup.find_all("product")[0]

        #데이터 값 추출
        ProductName=product.productname.contents[0]
        SellerNick=product.sellernick.contents[0]
        Seller=product.seller.contents[0]
        try:
            SellGrade=int(PI.sellgrade.contents[0])
        except:
            SellGrade="nan"
        try:
            SellSatisfaction=int(PI.sellsatisfaction.contents[0])
        except:
            SellSatisfaction="nan"
        
        try:
            BuySatisfy=int(product.buysatisfy.contents[0])
        except:
            BuySatisfy="nan"
        Rating=int(product.rating.contents[0])        
        ReviewCount=int(product.reviewcount.contents[0])
        
        ProductPrice=int(product.productprice.contents[0])
        SalePrice=int(product.saleprice.contents[0])
        Price=PI.productprice.price.contents[0]
        LowestPrice=PI.productprice.lowestprice.contents[0]
        
        BenefitDiscount=int(product.benefit.discount.contents[0])
        BenefitMileage=int(product.benefit.mileage.contents[0])
        Point=int(PI.point.contents[0])
        Chip=int(PI.chip.contents[0])

        #딕셔너리 입력
        Data_Origin[title][str(num)]={"ProductCode":ProductCode,"ProductName":ProductName,
                            "SellerNick":SellerNick,"Seller":Seller,
                            "SellGrade":SellGrade,
                            "SellSatisfaction":SellSatisfaction,"BuySatisfy":BuySatisfy,
                            "Rating":Rating,"ReviewCount":ReviewCount,
                            "ProductPrice":ProductPrice,"SalePrice":SalePrice,"Price":Price,"LowestPrice":LowestPrice,
                            "BenefitDiscount":BenefitDiscount,"BenefitMileage":BenefitMileage,
                            "Point":Point,"Chip":Chip}
        num += 1
    return Data_Origin,start_num,end_num,title,keyword
'''
[함수파라미터주석]
    apiCode0: 적용함수 
        → ProductSearch : 상품검색  (default)
        → ProductInfo : 상품정보조회
        → CategoryInfo : 카데고리 조회
            → productCode 파라미터를 넣으면 상품이미지 조회 

    keyword: 검색내용   categoryCode: 카테고리코드 , productCode: 상품코드

    pageNum: 검색할 페이지
    pageSize: 페이지당 검색수
    Category: 카데고리 구분시 작성
    sortCd: 정렬순서
            → CP : 인기도순
            → A : 누적판매순
            → G : 평가높은순
            → I : 후기/리뷰많은순
            → L : 낮은가격순
            → H : 높은가격순
            → N : 최근등록순

    [ProductSeartch 한정]
    targetSearchPrd: 상품검색대상
            → ENG : 영문상품
            → KOR : 국문상품
'''

#예제
'''
data_json={}
data=get_page(keyword="사과",pageNum=1,pageSize=50,sortCd="CP")
result=tojson_PS(data,data_json,start_num=0)
breakpoint()
'''

'''
[Result 파라미터 주석]
    [ProductSearch]
        #get_page(keyword="사과",pageNum=1,pageSize=50)
        #data[0].find_all("sellernick")

        productname,productcode,seller
        rating,reviewcount,buysatisfy
        productprice=saleprice
        benefit.discount 
        benefit.mileage

    [ProductInfo]
        #프로덕트코드
        productcode=int(data[0].productcode.contents[0])

        get_page(apiCode="ProductInfo",productCode=productcode)
        productcode, productname
        productprice.price
        productprice.lowestprice
        point,chip
        sellsatisfaction, sellgrade

    [CategoryInfo] 50000까진 자료있는듯
        #get_page(apiCode="CategoryInfo",categoryCode=0,pageNum=1,pageSize=50)[0].catagoryname.contents
        #data[0].categoryname.contents[0]
'''