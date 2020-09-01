if exists(select 1 from "sysobjects" where "xtype" = 'V' and "name" = 'AVA_IM_OPRC') drop view "AVA_IM_OPRC"
go

create view "AVA_IM_OPRC"
as
	select t0."ItemCode" "ItemCode",t0."DfltWH" "Warehouse",t0."AvgPrice" "Price",0 "PriceDiff" from "OITM" t0
	where t0."DfltWH" is not null 
go