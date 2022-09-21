NUM_ROWS = 1000000
noise_randomity = 3
noise = 0
DEFAULT_DIR = 'datasets/'
COLUMNS = [
    "Geo.continent",
    "Geo.country",
    "Geo.country_iso2",
    "Geo.country_iso3",
    "Geo.region",
    "Geo.region_iso",
    "Payment.method",
    "Product.category_1",
    "Product.category_2",
    "Product.category_3",
    "Product.category_4",
    "Product.category_5",
    "Product.category_6",
    "Product.category_7",
    "Product.category_8",
    "Shipper.society",
    "Time.day"
]

FILENAME = DEFAULT_DIR + 'dataset_'+str(NUM_ROWS)+'_10.csv'

#--CHILD--
NUM_ROWS_CHILD = 80000
inherited_rows_percentage = 50
CHILD_FILENAME = DEFAULT_DIR + 'child_dataset_'+str(NUM_ROWS)+'_'+str(NUM_ROWS_CHILD)+'_'+str(inherited_rows_percentage)+'.csv'