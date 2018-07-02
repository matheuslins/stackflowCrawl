hipotese1 = ("""

salary x tecnologies

db.getCollection('crawlpy_jobs').aggregate(
    [{
        "$group": {
            "_id": {
                salary: {"$ifNull": [ "$salary", false]},
                tecnologies: "$tecnologies"
            }
        }
    }]
)

job_type x count

db.getCollection('crawlpy_jobs').aggregate(
    [
        {"$group": {
            _id : "$job_type",
            count: {$sum: 1}
        }}
        
    ]
)

experience_level X count

db.getCollection('crawlpy_jobs').aggregate(
    [
        {"$group": {
            _id : "$experience_level",
            count: {$sum: 1}
        }}
        
    ]
)
""")


hipotese2 = ("""




""")
