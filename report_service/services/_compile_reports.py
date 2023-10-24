from adapters.databases import Mongo
from adapters.models import OutputData


async def compile_reports(mongo: Mongo, phones_list: list[int] = None):

    aggregate_expr = [
       {"$project": {
           "phone": 1,
           "secs": {"$divide": [{"$subtract": ["$end_date", "$start_date"]}, 1000]}
       }},
       {"$group": {
""
           "_id": { "phone": '$phone' },
           "cnt_all_attempts": { "$sum": 1 },
           "avg_dur_att": { "$avg": "$secs" },
           "min_dur": { "$min": "$secs" },
           "max_dur": { "$max": "$secs" },

           "10_sec": {"$sum": {"$cond": [{"$lte": ["$secs", 10]}, 1, 0]}},
           "10_30_sec": {"$sum": {"$""cond": [{"$and": [{"$lte": ["$secs", 30]}, {"$gt": ["$secs", 10]}]}, 1, 0]}},
           "30_sec": {"$sum": {"$cond": [{"$gt": ["$secs", 30]}, 1, 0]}},
           "sum_price_att_over_15": {"$sum": {"$cond": [{"$gt": ["$secs", 15]}, {"$multiply": ["$secs", 10]}, 0]}},
       }},
       {"$project": {
           "phone": "$_id.phone",
           "cnt_all_attempts": 1,
           "avg_dur_att": 1,
           "min_price_att": {"$multiply": ["$min_dur", 10]},
           "max_price_att": {"$multiply": ["$max_dur", 10]},
           "cnt_att_dur": {
                "10_sec": "$10_sec",
                "10_30_sec": "$10_30_sec",
                "30_sec": "$30_sec"
           },
           "sum_price_att_over_15": 1,
           }}
    ]

    if phones_list:
        aggregate_expr.insert(0, {"$match": {"phone": {"$in": phones_list}}})

    reports: list[OutputData] = []
    raw_reports = mongo.data_collection.aggregate(aggregate_expr)
    async for raw_report in raw_reports:
        reports.append(OutputData.model_validate(raw_report))

    return reports
