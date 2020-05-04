""" 
    Performs report per department 
    How many orders from department and how many first orders
    
    Usage:
        python3 python purchase_analytics.py order_table product_table report_output
    order_table   -- Orders table with details    
    product_table -- Products table with details
    report_output -- Report file
"""

from pathlib import Path
import itertools as itts
import csv
import sys
from operator import itemgetter

from typing import List, Dict, Set

# _MAIN_LOC = Path("/home/saveliy/InsightData/Purchase-Analytics")
# _TEST_LOC = _MAIN_LOC / "insight_testsuite/tests/test_2"
# _INPUT_LOC = _TEST_LOC / "input"
# _OUTPUT_LOC = _TEST_LOC / "output"

#
# _INFILE_ORDER = _INPUT_LOC / "order_products.csv"
# _INFILE_ORDER = _INPUT_LOC / "order_products__prior.csv"
# _INFILE_PRODUCT = _INPUT_LOC / "products.csv"
# _OUTFILE_REPORT = _OUTPUT_LOC / "report_1.csv"


def read_table(InFile: Path, ColumnToKeep: Set = None) -> List[Dict]:
    """Reads table from csv file
    Arguments:
        InFile {Path} -- path to file
        ColumnToKeep {Set} -- Columns to keep if None keeps all columns
    Returns:
        List[Dict] -- list of rows each row is a dict 
    """
    out_data = []
    with open(InFile) as oF:
        reader = csv.reader(oF, delimiter=",")
        header_line = next(reader)
        # lazy inlude all columns to keep
        if ColumnToKeep is None:
            ColumnToKeep = set(header_line)
        for line in itts.islice(reader, 0, None):
            out_data.append(
                {k: v for k, v in zip(header_line, line) if k in ColumnToKeep}
            )
    return out_data


def combine_tables(Orders: List[Dict], Products: List[Dict]):
    """ 
    Add department column to order data 
    if product from order not in product table set departmnet to None
    Orders table is updated
    Arguments:
        Orders {List[Dict]} -- order table
        Products {List[Dict]} -- product table
    """
    product_dict = {l["product_id"]: l["department_id"] for l in Products}
    for order in Orders:
        # checks if product_id in Product table
        if order["product_id"] in product_dict:
            order.update({"department_id": product_dict[order["product_id"]]})
        else:
            order.update({"department_id": None})


def get_statistics(Orders: List[Dict]) -> List[Dict]:
    """ 
        Get statistics per department
        Department id
        Number of times was a product requested from this department
        Number of requests contain products ordered for the first time
        Percentage. Of first requests
    Arguments:
        Orders {List[Dict]} -- List of products from orders table
    Returns:
        List[Dict] -- Report Table List of Dict
    """

    def _sort_dep(R):
        """ Help fnx to sort rows by int of department id """
        return int(R["department_id"])

    report = []
    # sort orders by department drops None
    srt_order = sorted(
        filter(lambda x: x["department_id"] is not None, Orders), key=_sort_dep,
    )
    for dep, dep_gr in itts.groupby(srt_order, key=itemgetter("department_id")):
        reorders = [int(x["reordered"]) for x in dep_gr]
        # skip zero orders from departemnt should not be the case but still
        if len(reorders) == 0:
            continue
        total_order = len(reorders)
        num_frst_order = total_order - sum(reorders)
        report.append(
            {
                "department_id": dep,
                "number_of_orders": total_order,
                "number_of_first_orders": num_frst_order,
                "percentage": "{:.2f}".format(num_frst_order / float(total_order)),
            }
        )
    return report


if __name__ == "__main__":
    # input files
    _INFILE_ORDER = sys.argv[1]
    _INFILE_PRODUCT = sys.argv[2]
    _OUTFILE_REPORT = sys.argv[3]

    # reads input data
    order_data = read_table(
        _INFILE_ORDER, ColumnToKeep=set(["product_id", "reordered"])
    )
    product_data = read_table(
        _INFILE_PRODUCT, ColumnToKeep=set(["product_id", "department_id"])
    )
    # combining tables
    combine_tables(order_data, product_data)
    # get report
    report = get_statistics(Orders=order_data)
    header = [
        "department_id",
        "number_of_orders",
        "number_of_first_orders",
        "percentage",
    ]
    # output report
    with open(_OUTFILE_REPORT, "w", newline="") as oF:
        csvWriter = csv.DictWriter(oF, fieldnames=header)
        csvWriter.writeheader()
        csvWriter.writerows(report)
