import pandas as pd
import os
from typing import Optional, Tuple

class AWSICSControlMapper:
    def __init__(self, aws_path: str, master_path: str):
        """
        Initializes the AWSICSControlMapper with AWS and master file paths.

        :param aws_path: The path to the AWS Excel file.
        :param master_path: The path to the master Excel file.
        """
        self.aws_df = self.read_excel_file(aws_path)
        self.master_df = self.read_excel_file(master_path)

    def read_excel_file(self, file_path: str) -> Optional[pd.DataFrame]:
        """
        Reads an Excel file and returns a pandas DataFrame.

        :param file_path: The path to the Excel file.
        :return: A pandas DataFrame containing the data from the Excel file, or None if an error occurs.
        """
        try:
            df = pd.read_excel(file_path)
            return df
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None

    def map_control_title_to_l2_id(self, control_title: str) -> Optional[str]:
        """
        Maps the control title to the L2 ID using the AWS DataFrame.

        :param control_title: The control title to map.
        :return: The L2 ID if found, otherwise None.
        """
        try:
            l2_id = self.aws_df.loc[self.aws_df['L4 Control Name'] == control_title, 'L2 ID']
            if not l2_id.empty:
                return l2_id.iloc[0]
            else:
                print(f"L2 ID not found for Control Title: {control_title}")
                return None
        except Exception as e:
            print(f"Error mapping control title to L2 ID: {e}")
            return None

    def map_l2_id_to_control_domain(self, l2_id: str) -> Optional[str]:
        """
        Maps the L2 ID to the control domain using the master DataFrame.

        :param l2_id: The L2 ID to map.
        :return: The control domain if found, otherwise None.
        """
        try:
            control_domain = self.master_df.loc[self.master_df['Statement Index'] == l2_id, 'Control Domain']
            if not control_domain.empty:
                return control_domain.iloc[0]
            else:
                print(f"Control Domain not found for L2 ID: {l2_id}")
                return None
        except Exception as e:
            print(f"Error mapping L2 ID to control domain: {e}")
            return None

    def get_l2_id_and_control_domain(self, control_title: str) -> Optional[Tuple[str, str]]:
        """
        Gets the L2 ID and control domain for a given control title.

        :param control_title: The control title to map.
        :return: A tuple of (L2 ID, Control Domain) if both are found, otherwise None.
        """
        l2_id = self.map_control_title_to_l2_id(control_title)
        if l2_id is not None:
            control_domain = self.map_l2_id_to_control_domain(l2_id)
            if control_domain is not None:
                return l2_id, control_domain
        return None

pip install pandas sqlalchemy python-dotenv psycopg2-binary


from db.database import create_engine_instance
from db.models import Base

def setup_database() -> None:
    """
    Set up the database by creating tables if they don't exist.
    """
    engine = create_engine_instance()
    Base.metadata.create_all(engine)



import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base

def get_db_url() -> str:
    """
    Get the database URL from the system environment variable.
    
    :return: Database URL string.
    """
    return os.getenv('DATABASE_URL')

def create_engine_instance() -> create_engine:
    """
    Create and return a SQLAlchemy engine instance.
    
    :return: SQLAlchemy engine instance.
    """
    db_url = get_db_url()
    if db_url is None:
        raise ValueError("DATABASE_URL environment variable is not set.")
    return create_engine(db_url)

def create_session() -> sessionmaker:
    """
    Create and return a SQLAlchemy sessionmaker instance bound to the engine.
    
    :return: SQLAlchemy sessionmaker instance.
    """
    engine = create_engine_instance()
    return sessionmaker(bind=engine)
