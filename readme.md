> index.py
- 메인 실행 로직

- 필요한 기본 데이터
    - data/farm_source_info.csv : 메인 정보 파일(pk,비교용데이터 두개 컬럼 사용)
    - 대조군 폴더 구조  
    -- data/asan/outco/농약사/날짜/파일명  
    -- data/asan/outsales/농약사/날짜/파일명  
    -- data/woosung/outco/농약사/날짜/파일명  
    -- data/woosung/outsales/농약사/날짜/파일명  
 

 
    
> recovery.py
- csv 파일 내에 \0 가 있거나 특정 오류 문자열 복구용 로직
