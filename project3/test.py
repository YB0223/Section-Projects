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