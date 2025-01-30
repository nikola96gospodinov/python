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
def create_example_tables_with_data():
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

create_example_tables_with_data()

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
            if isinstance(self._selected_columns, str):
                self._selected_columns = list(args)
            self._selected_columns.extend(list(args))
        
        return self
    
    def avg(self, *args: Union[str, ColumnSelector]) -> 'QueryBuilder':
        """
        Add AVG aggregate function
        Example: avg("salary", { "column": "bonus", "alias": "average_bonus" })
        Results: AVG(salary), AVG(bonus) AS average_bonus
        """
        if args:
            self._avg.extend(list(args))
        
        return self
    
    def sum(self, *args: Union[str, ColumnSelector]) -> 'QueryBuilder':
        """
        Add SUM aggregate function
        Example: sum("salary", { "column": "bonus", "alias": "total_bonus" }))
        Results: SUM(salary), SUM(bonus) as total_bonus
        """
        if args:
            self._sum.extend(list(args))
        
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
            
        return self
        
    def order_by(self, fields: List[Union[OrderBySelector, str]]) -> 'QueryBuilder':
        """
        Add ORDER BY clause
        Example: order_by([name, { "column": "age", "is_desc": TRUE }])
        Results: ORDER BY name, age DESC
        """
        self._order_by.extend(fields)
        return self
    
    def group_by(self, *args: str) -> 'QueryBuilder':
        """
        Add GROUP BY clause
        Example: group_by("department")
        Results: GROUP BY department
        """
        self._group_by.extend(args)
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
    
    def _validate_columns_existence(self, column_and_fk_names: List[str]) -> bool:
        """Check if all the column names and fks passed are valid"""
        return True
    
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
        conditions = []
        
        for field, details in self._where_conditions.items():
            operator = details["operator"]
            value = self._format_value(details["value"])
            conditions.append(f"{field} {operator} {value}")
            
        sql = "SELECT * FROM some_table"
        
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
            
        # if self._order_by:
        #     sql += " ORDER BY " + ", ".join(self._order_by)
            
        if self._limit_value:
            sql += f" LIMIT {self._limit_value}"
            
        return sql
    