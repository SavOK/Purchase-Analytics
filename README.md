# Purchase-Analytics


## Problem

Instacart has published a [dataset](https://www.instacart.com/datasets/grocery-shopping-2017) containing 3 million Instacart orders.

**Prepare the report** for each department:, 
+ the number of times a product was requested
+ number of times a product was requested for the first time 
+ a ratio of those two numbers.


## Usage 
```bash
python3 ./src/purchase_analytics.py order_table product_table report_file
```

## Input files
### Order Table 
**IMPORTANT**:
* data must be in comma separated text file
* first line must be header line
* must have this columns
 
| column     | description                                                                    | type/format |
| ---------- | ------------------------------------------------------------------------------ | ----------- |
| product_id | unique product id                                                              | `int`       |
| reordered  | flag if the product has been ordered by this user in the past **0: no 1: yes** | `int`       |

### Product Table
**IMPORTANT**:
* data must be in comma separated text file
* first line must be header line
* must have this columns
 
| column        | description                  | type/format |
| ------------- | ---------------------------- | ----------- |
| product_id    | unique product id            | `int`       |
| department_id | identifier of the department | `int`       |


### Report File
* `department_id` Department idetifier
* `number_of_orders`. Number of times  product requested from this department.
* `number_of_first_orders`. Number of  requests contain products ordered for the first time.
* `percentage`. Percentage of requests containing products ordered for the first time compared with the total number of requests for products from that department (rounded to `.2f`).

## Solution
The solution is implemented in python 3.5+
with standard python libraries ([`itettols`](https://docs.python.org/3.5/library/itertools.html),
[`scv`](https://docs.python.org/3.5/library/csv.html))

                       