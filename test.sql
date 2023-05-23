
-- 2021/10/20 7macro에 대한 상담사 코멘트
--   (Zendesk에서 깃발 버튼 눌러서 상담사들이 남긴 내용 호출 쿼리)

SELECT
	cfs.ticketid,
	cfs.createdat,
	cfs.ticketfieldid,
	cfs.name,
	cfs.value AS comment,
	csa.media_type_code,
	csa.inquiry_category_code3,
	csa.agent_id,
	cate.fullname
FROM ODS.zendesk_ticket_custom_field_split AS cfs
LEFT JOIN SB_FCSYSTEMS.dhf_csa_inquiry_hourly AS csa ON cfs.ticketid = csa.inquiry_id
LEFT JOIN ODS.COUNSELING_CATEGORIES AS cate ON csa.inquiry_category_code3 = cate.categorycode
WHERE 1=1
	AND ticketfieldid = 360023001233
	AND date_format(ticketcreatedat,'%Y%m%d') between '20211005' and '20211007'
	AND csa.basis_dt between 20211005 and 20211007;
