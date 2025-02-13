from typing import List, Any, Optional, Dict, Union, Literal
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

class SQLDataType(Enum):
    INT = "INT"
    DATETIME = "DATETIME"
    TEXT = "TEXT"
    DECIMAL = "DECIMAL"
    BOOLEAN = "BOOLEAN"
    FLOAT = "FLOAT"
    DATE = "DATE"
    BIGINT = "BIGINT"

validators = {
    SQLDataType.BIGINT: lambda v: v.isdigit(),
    SQLDataType.INT: lambda v: v.isdigit(),
    SQLDataType.BOOLEAN: lambda v: v.upper() in ("TRUE", "FALSE"),
    SQLDataType.FLOAT: lambda v: v.replace(".", "", 1).isdigit(),
    SQLDataType.DECIMAL: lambda v: v.replace(".", "", 1).isdigit()
}
    
@dataclass
class Column:
    """Represents a database column with its properties"""
    name: str
    data_type: SQLDataType
    default_value: Optional[Any] = None
    is_pk: bool = False
    auto_increment: bool = False
    not_null: bool = False
    unique: bool = False
    
@dataclass    
class ForeignKey:
    """Represents a foreign key column in the database"""
    name: str
    reference_table_name: str
    reference_column_name: str
    
class ColumnRepository:
    def __init__(self) -> None:
        self._columns: List[Column] = []
        self._foreign_keys: List[ForeignKey] = []
        
    @property
    def columns(self):
        return self._columns
    
    @property
    def foreign_keys(self):
        return self._foreign_keys
        
    def _validate_auto_increment(self, column: Column) -> None:
        """Validate auto increment constraints"""
        if column.auto_increment:
            if not column.is_pk:
                raise ValueError("AUTO_INCREMENT can only be used with PRIMARY KEY")
            if column.data_type not in (SQLDataType.INT, SQLDataType.BIGINT):
                raise ValueError("AUTO_INCREMENT can only be used with INT or BIGINT data types")
            
    def _validate_default_value(self, column: Column) -> None:
        """Validate default value matches column type"""
        if column.default_value is None:
            return
        
        value = str(column.default_value)
        
        try:
            validator = validators[column.data_type]
            if not validator(value):
                raise ValueError(f"Invalid default value '{value}' for type {column.data_type.value}")
        except:
            return
            
    def add_column(
        self,
        name: str,
        data_type: Union[SQLDataType, str],
        default_value: Optional[Any] = None,
        is_pk: bool = False,
        auto_increment: bool = False,
        not_null: bool = False,
        unique: bool = False
    ) -> 'ColumnRepository':
        """
        Add a column to the repository. Returns self for method chaining.
        
        Args:
            name: Column name
            data_type: SQLDataType or string representation of SQL type
            default_value: Default value for the column
            is_pk: Whether this is a primary key
            auto_increment: Whether this should auto increment
            not_null: Whether this column can be null
            unique: Whether this column should be unique
        
        Raises:
            ValueError: If column validation fails
        """
        
        if name in [column.name for column in self._columns] or name in [key.name for key in self._foreign_keys]:
            raise ValueError(f"Column '{name}' already exists in table")
        
        if isinstance(data_type, str):
            try:
                data_type = SQLDataType(data_type.upper())
            except ValueError:
                raise ValueError(
                    f"Invalid data type. Must be one of: {', '.join(t.value for t in SQLDataType)}"
                )
                
        column = Column(
            name=name,
            data_type=data_type,
            default_value=default_value,
            is_pk=is_pk,
            auto_increment=auto_increment,
            not_null=not_null,
            unique=unique
        )
        
        self._validate_auto_increment(column)
        self._validate_default_value(column)
        
        self._columns.append(column)
        return self
    
    def remove_column(self, column_name: str) -> bool:
        found_column = next((column for column in self._columns if column.name == column_name), None)
        
        if found_column:
            self._columns.remove(found_column)
            return True
        
        print("Column doesn't exist")
        return False
    
    def add_foreign_key(
        self,
        name: str,
        reference_table_name: str,
        reference_column_name: str
    ) -> 'ColumnRepository':
        """
        Add a foreign key constraint. Returns self for method chaining.
        """
        
        if name in [column.name for column in self._columns] or name in [key.name for key in self._foreign_keys]:
            raise ValueError(f"Column '{name}' already exists in table")
        
        fk = ForeignKey(name, reference_table_name, reference_column_name)
        self._foreign_keys.append(fk)
        return self
    
    def remove_foreign_key(self, key_name: str) -> bool:
        found_key = next((key for key in self._foreign_keys if key.name == key_name), None)
        
        if found_key:
            self._foreign_keys.remove(found_key)
            return True
        
        print("Foreign key doesn't exist")
        return False 
    
class Row:
    def __init__(self, columns: List[Column], foreign_keys: List[ForeignKey], values: Dict[str, Any]) -> None:
       # Get required column names from not_null columns and foreign keys
        required_columns = [column.name for column in columns 
                          if column.not_null and column.default_value is None]
        fk_columns = [key.name for key in foreign_keys]
        all_required_values = required_columns + fk_columns
        
        # Check all required values are provided
        missing_values = [name for name in all_required_values 
                         if name not in values or values[name] is None]
        if missing_values:
            raise ValueError(f"Missing required values for columns: {', '.join(missing_values)}")
        
        # Validate data types
        for column in columns:
            if column.name in values:
                value = values[column.name]
                if not self._validate_type(value, column.data_type):
                    raise ValueError(f"Invalid type for column {column.name}: expected {column.data_type.value}")
        
        self._values = values
        
    @property
    def values(self):
        return self._values
    
    def _validate_type(self, value: Any, data_type: SQLDataType) -> bool:
        if value is None:
            return True # Already checked if the value us required
        
        converted_value = str(value)
        
        try:
            validator = validators[data_type]
            if not validator(converted_value):
                print(f"Invalid value '{converted_value}' for type {data_type.value}")
                return False
        except:
            # If we can't find a validator for the data type it should pass
            return True
        
        return True

class RowRepository:
    def __init__(self) -> None:
        self._rows: List[Row] = []
        
    def add_row(self, values: Dict[str, Any], columns: List[Column], foreign_keys: List[ForeignKey]) -> bool:
        try:
            new_row = Row(columns, foreign_keys, values)
            self._rows.append(new_row)
            return True
        except:
            print(f"Failed to create a row with values: {values}")
            return False
        
    def remove_row(self, row: Row) -> bool:
        if row in self._rows:
            self._rows.remove(row)
            return True
        
        print("Row doesn't exist")
        return False

class Table:
    def __init__(self, table_name: str, column_repository: ColumnRepository, row_repository: RowRepository) -> None:
        self.table_name: str = table_name
        self.column_repository = column_repository
        self.row_repository = row_repository
        
    def add_column(
        self,
        name: str,
        data_type: Union[SQLDataType, str],
        default_value: Optional[Any] = None,
        is_pk: bool = False,
        auto_increment: bool = False,
        not_null: bool = False,
        unique: bool = False    
    ) -> 'Table':
        try:
            self.column_repository.add_column(
                name=name,
                data_type=data_type,
                default_value=default_value,
                is_pk=is_pk,
                auto_increment=auto_increment,
                not_null=not_null,
                unique=unique
            )
        except Exception as error:
            print(f"Something went wrong: {error}")
            
        return self
    
    def remove_column(self, column_name: str) -> 'Table':
        valid_columns = [col.name for col in self.column_repository.columns]
        
        if column_name not in valid_columns:
            print(f"Invalid column name. Must be one of: {', '.join(valid_columns)}")
            return self
        
        self.column_repository.remove_column(column_name)
        return self
    
    def add_foreign_key(
        self,
        name: str,
        reference_table: 'Table',
        reference_column_name: str
    ) -> 'Table':
        found_reference = next((col for col in reference_table.column_repository.columns if col.name == reference_column_name), None)
        
        if found_reference:
            try:
                self.column_repository.add_foreign_key(name, reference_table.table_name, reference_column_name)
            except Exception as error:
                print(f"Something went wrong: {error}")
        else:
            print(f"{reference_column_name} doesn't exist in the {reference_table.table_name} table")
        
        return self
    
    def remove_foreign_key(self, key_name: str) -> 'Table':
        try:
            self.column_repository.remove_foreign_key(key_name)
        except Exception as error:
            print(f"Something went wrong: {error}")
        
        return self
    
    def add_row(self, values: Dict[str, Any]) -> 'Table':
        self.row_repository.add_row(values, self.column_repository.columns, self.column_repository.foreign_keys)
        
        return self
    
    def remove_row(self, row: Row) -> 'Table':
        self.row_repository.remove_row(row)
        
        return self
    
    def _format_column(self, column: Column) -> str:
        """Format a column definition as SQL"""
        parts = [
            column.name,
            column.data_type.value
        ]
        
        if column.default_value is not None:
            parts.append(f"DEFAULT {column.default_value}")
        if column.is_pk:
            parts.append("PRIMARY KEY")
        if column.auto_increment:
            parts.append("AUTO_INCREMENT")
        if column.not_null:
            parts.append("NOT NULL")
        if column.unique:
            parts.append("UNIQUE")
            
        return " ".join(parts)
    
    def _format_foreign_key(self, foreign_key: ForeignKey) -> str:
        """Format a foreign key"""
        return f"FOREIGN KEY ({foreign_key.name}) REFERENCES {foreign_key.reference_table_name}({foreign_key.reference_column_name})"
    
    def __str__(self) -> str:
        """Generate SQL CREATE TABLE statement"""
        parts = [self._format_column(column) for column in self.column_repository.columns]
        parts.extend([self._format_foreign_key(key) for key in self.column_repository.foreign_keys])
        
        return f"CREATE TABLE {self.table_name} (\n    " + ",\n    ".join(parts) + "\n)"

def create_table(table_name: str) -> 'Table':
    column_repo = ColumnRepository()
    row_repo = RowRepository()
    table = Table(table_name, column_repo, row_repo)
    return table

# Example tables
# Create users table
users = create_table("users")
users.add_column("id", SQLDataType.INT, is_pk=True, auto_increment=True)
users.add_column("username", SQLDataType.TEXT, not_null=True, unique=True)
users.add_column("email", SQLDataType.TEXT, not_null=True)
users.add_column("created_at", SQLDataType.DATETIME, default_value="CURRENT_TIMESTAMP")

# Add some user rows
users.add_row({
    "username": "john_doe",
    "email": "john@example.com"
})
users.add_row({
    "username": "jane_smith", 
    "email": "jane@example.com"
})

# Create orders table with foreign key to users
orders = create_table("orders")
orders.add_column("id", SQLDataType.INT, is_pk=True, auto_increment=True)
orders.add_column("total", SQLDataType.DECIMAL, not_null=True)
orders.add_column("order_date", SQLDataType.DATETIME, default_value="CURRENT_TIMESTAMP")
orders.add_foreign_key("user_id", users, "id")

# Add some order rows
orders.add_row({
    "user_id": 1,
    "total": "99.99"
})
orders.add_row({
    "user_id": 2,
    "total": "149.99"
})

# Create products table
products = create_table("products")
products.add_column("id", SQLDataType.INT, is_pk=True, auto_increment=True) 
products.add_column("name", SQLDataType.TEXT, not_null=True)
products.add_column("price", SQLDataType.DECIMAL, not_null=True)
products.add_column("stock", SQLDataType.INT, default_value="0")

# Add some product rows
products.add_row({
    "name": "Laptop",
    "price": "999.99",
    "stock": 50
})
products.add_row({
    "name": "Mouse",
    "price": "24.99",
    "stock": 100
})

EQ = "eq"
GT = "gt"
LT = "lt"
GTE = "gte"
LTE = "lte"
LIKE = "like"
IN = "in"

operators = {
    EQ: '=',
    GT: '>',
    LT: '<',
    GTE: '>=',
    LTE: '<=',
    LIKE: 'LIKE',
    IN: 'IN'
}

@dataclass
class ColumnSelector:
    column: str
    alias: Optional[str]
    
@dataclass
class OrderBySelector:
    column: str
    is_desc: bool = False

class QueryBuilder:
    def __init__(self, table: Table) -> None:
        self.table = table
        self._selected_columns: List[Union[ColumnSelector, str]] | Literal["*"] = "*"
        self._avg: List[Union[ColumnSelector, str]] = []
        self._sum: List[Union[ColumnSelector, str]] = []
        self._where_conditions: Dict[str, Any] = {}
        self._group_by: List[str] = []
        self._order_by: List[Union[OrderBySelector, str]] = []
        self._limit_value: Optional[int] = None
        self._offset_value: Optional[int] = None
        self._is_distinct: bool = False
        
    def _transform_column_selector_union_to_str(self, args: tuple[Union[str, ColumnSelector | OrderBySelector], ...]) -> List[str]:
        all_columns_and_fks_passed: List[str] = []
        for arg in args:
            if isinstance(arg, str):
                all_columns_and_fks_passed.append(arg)
            else:
                all_columns_and_fks_passed.append(arg.column)
        return all_columns_and_fks_passed
    
    def _validate_columns_existence(self, column_and_fk_names: List[str]) -> bool:
        """Check if all the column names and fks passed are valid"""
        all_column_names = [column.name for column in self.table.column_repository.columns]
        all_fk_names = [fk.name for fk in self.table.column_repository.foreign_keys]
        all_possible_columns = all_column_names + all_fk_names
        
        return all(column for column in column_and_fk_names if column in all_possible_columns)
        
    def select(self, *args: Union[str, ColumnSelector]) -> 'QueryBuilder':
        """
        Add SELECT clause
        
        Example 1: select() or select(*)
        Result 1: SELECT *
        
        Example 2: select("id", "name")
        Result 2: SELECT id, name
        
        Example 3: select("id", { "column": "name", "alias": "first_name" })
        Result 3: SELECT id, name as first_name
        """
        if args:
            all_columns_and_fks_passed = self._transform_column_selector_union_to_str(args)
            is_input_valid = self._validate_columns_existence(all_columns_and_fks_passed)
            
            if is_input_valid:
                if isinstance(self._selected_columns, str):
                    self._selected_columns = list(args)
                else:
                    self._selected_columns.extend(list(args))
            else:
                print("Make sure you pass only existing columns and foreign keys to SELECT")
        
        return self
    
    def avg(self, *args: Union[str, ColumnSelector]) -> 'QueryBuilder':
        """
        Add AVG aggregate function
        Example: avg("salary", { "column": "bonus", "alias": "average_bonus" })
        Results: AVG(salary), AVG(bonus) AS average_bonus
        """
        if args:
            all_columns_and_fks_passed = self._transform_column_selector_union_to_str(args)
            is_input_valid = self._validate_columns_existence(all_columns_and_fks_passed)
            
            if is_input_valid:
                self._avg.extend(list(args))
            else:
                print("Cannot AVG properties that don't exist")
        
        return self
    
    def sum(self, *args: Union[str, ColumnSelector]) -> 'QueryBuilder':
        """
        Add SUM aggregate function
        Example: sum("salary", { "column": "bonus", "alias": "total_bonus" }))
        Results: SUM(salary), SUM(bonus) as total_bonus
        """
        if args:
            all_columns_and_fks_passed = self._transform_column_selector_union_to_str(args)
            is_input_valid = self._validate_columns_existence(all_columns_and_fks_passed)
            
            if is_input_valid:
                self._sum.extend(list(args))
            else:
                print("Cannot SUM properties that don't exist")
        
        return self
        
    def distinct(self, is_distinct: bool) -> 'QueryBuilder':
        """
        Add DISTINCT to a SELECT
        Example: distinct(True)
        Results: SELECT DISTINCT ...
        """
        self._is_distinct = is_distinct        

        return self
    
    def where(self, **kwargs: Any) -> 'QueryBuilder':
        """
        Add WHERE clause
        Example: where(name="John", age__gt=25)
        Results: WHERE name = "John" AND age > 25
        """
        all_keys = [key for key, value in kwargs.items()]
        is_input_valid = self._validate_columns_existence(all_keys)
        
        if is_input_valid:
            for key, value in kwargs.items():
                # Handle special operators (e.g., age__gt=25)
                if "__" in key:
                    field, operator = key.split("__")
                    if operator in operators:
                        self._where_conditions[field] = {
                            "operator": operators[operator],
                            "value": value
                        }
                else:
                    # Handle simple equality
                    self._where_conditions[key] = {
                        "operator": "=",
                        "value": value
                    }
        else:
            print("Make sure you pass only existing fields to your WHERE clause")
            
        return self
        
    def order_by(self, *args: Union[str, OrderBySelector]) -> 'QueryBuilder':
        """
        Add ORDER BY clause
        Example: order_by(name, { "column": "age", "is_desc": TRUE })
        Results: ORDER BY name, age DESC
        """
        if args:
            all_columns_and_fks_passed = self._transform_column_selector_union_to_str(args)
            is_input_valid = self._validate_columns_existence(all_columns_and_fks_passed)
            
            if is_input_valid:
                self._order_by.extend(list(args))
            else:
                print("Cannot ORDER BY properties that don't exist")
                
        return self
    
    def group_by(self, *args: str) -> 'QueryBuilder':
        """
        Add GROUP BY clause
        Example: group_by("department")
        Results: GROUP BY department
        """
        if args:
            all_columns_and_fks_passed = self._transform_column_selector_union_to_str(args)
            is_input_valid = self._validate_columns_existence(all_columns_and_fks_passed)
            
            if is_input_valid:
                self._group_by.extend(list(args))
            else:
                print("Cannot GROUP BY properties that don't exist")
                
        return self
    
    def limit(self, value: int) -> 'QueryBuilder':
        """
        Add LIMIT clause
        Example: limit(5)
        Results: LIMIT 5
        """
        self._limit_value = value
        return self
    
    def offset(self, value: int) -> 'QueryBuilder':
        """
        Add OFFSET clause
        Example: offset(10)
        Results OFFSET 10
        """
        self._offset_value = value
        return self
    
    def _format_value(self, value: Any) -> str:
        """Format values based on their type"""
        if isinstance(value, str):
            return f"'{value}'"
        elif isinstance(value, datetime):
            return f"'{value.strftime("%Y-%m-%d %H:%M:%S")}'"
        elif isinstance(value, (list, tuple)):
            return f"({", ".join(map(self._format_value, value))})"
        return str(value)
    
    def __str__(self) -> str:
        """Convert the query to SQL string"""
        distinct = "DISTINCT " if self._is_distinct else ""
        
        if self._selected_columns == "*":
            sql = f"SELECT {distinct}*"
        else:
            select_conditions: List[str] = []
            
            for condition in self._selected_columns:
                if isinstance(condition, str):
                    select_conditions.append(condition)
                else:
                    if condition.alias:
                        select_conditions.append(f"{condition.column} AS {condition.alias}")
                    else:
                        select_conditions.append(condition.column)
                        
            for condition in self._avg:
                if isinstance(condition, str):
                    select_conditions.append(f"AVG({condition})")
                else:
                    if condition.alias:
                        select_conditions.append(f"AVG({condition.column}) AS {condition.alias}")
                    else:
                        select_conditions.append(f"AVG({condition.column})")
                        
            for condition in self._sum:
                if isinstance(condition, str):
                    select_conditions.append(f"SUM({condition})")
                else:
                    if condition.alias:
                        select_conditions.append(f"SUM({condition.column}) AS {condition.alias}")
                    else:
                        select_conditions.append(f"SUM({condition.column})")
            
            sql = f"SELECT {distinct}{", ".join(select_conditions)}"
            
        sql += f"\nFROM {self.table.table_name}"
        
        if self._where_conditions:
            where_conditions: List[str] = []
             
            for field, details in self._where_conditions.items():
                operator = details["operator"]
                value = self._format_value(details["value"])
                where_conditions.append(f"{field} {operator} {value}")
                
            sql += "\nWHERE " + " AND ".join(where_conditions)
            
        if self._group_by:
            sql +="\nGROUP BY " + ", ".join(self._group_by)
            
        if self._order_by:
            order_by_conditions: List[str] = []
            
            for condition in self._order_by: # type: ignore
                if isinstance(condition, str):
                    order_by_conditions.append(condition)
                elif isinstance(condition, OrderBySelector):
                    if condition.is_desc:
                        order_by_conditions.append(f"{condition.column} DESC")
                    else:
                        order_by_conditions.append(condition.column)
            
            sql += "\nORDER BY " + ", ".join(order_by_conditions)
            
        if self._limit_value:
            sql += f"\nLIMIT {self._limit_value}"
            
        if self._offset_value:
            sql += f"\nOFFSET {self._offset_value}"
            
        return sql

def test_query_builder():
    # Basic query
    qb = QueryBuilder(users)
    qb.select("name", "email")
    print(qb)
    print("\n")
    
    # Query with multiple conditions
    qb = QueryBuilder(orders)
    qb.select("id", "total").where(total__gt=100).order_by("created_at").limit(10)
    print(qb)
    print("\n")

    # Query with aggregations and grouping
    qb = QueryBuilder(products)
    qb.select("category").avg("price").sum("quantity").group_by("category")
    print(qb)
    print("\n")

    # Edge case: empty select
    qb = QueryBuilder(users)
    print(qb)
    print("\n")
    
    # Query with distinct values
    qb = QueryBuilder(users)
    qb.select("country").distinct(True)
    print(qb)
    print("\n")

    # Query with multiple aggregations and aliases
    qb = QueryBuilder(orders)
    qb.select("status").avg(ColumnSelector("total", "avg_total")).sum(ColumnSelector("total", "sum_total")).group_by("status")
    print(qb)
    print("\n")

    # Query with complex ordering
    qb = QueryBuilder(products)
    qb.select("name", "price", "stock").order_by(OrderBySelector("price", True), OrderBySelector("stock", True)).limit(5)
    print(qb)
    print("\n")

    # Query with offset pagination
    qb = QueryBuilder(users)
    qb.select("username", "email").order_by("username").limit(10).offset(20)
    print(qb)
    print("\n")

if __name__ == "__main__":
    test_query_builder()
