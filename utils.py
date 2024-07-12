import os
import pandas as pd
from aws_ics_control_mapper import AWSICSControlMapper
from db.setup import setup_database
from db.database import create_session
from db.models import AwsEc2TipControl

def process_tip_files(tip_folder: str, aws_path: str, master_path: str, output_folder: str) -> None:
    """
    Processes TIP files by reading them from a folder, mapping control titles to L2 IDs and control domains,
    and saving the updated files to a separate folder.

    :param tip_folder: The folder containing TIP Excel files.
    :param aws_path: The path to the AWS Excel file.
    :param master_path: The path to the master Excel file.
    :param output_folder: The folder to save the updated TIP Excel files.
    """
    mapper = AWSICSControlMapper(aws_path, master_path)
    Session = create_session()

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    tip_files = [os.path.join(tip_folder, f) for f in os.listdir(tip_folder) if f.endswith('.xlsx')]

    for tip_file in tip_files:
        try:
            tip_df = pd.read_excel(tip_file)
            tip_df['ICS ID'] = tip_df['Control Title'].apply(lambda x: mapper.map_control_title_to_l2_id(x))
            tip_df['ICS Control Area'] = tip_df['ICS ID'].apply(lambda x: mapper.map_l2_id_to_control_domain(x) if x else None)
            
            # Save to database
            with Session() as session:
                for index, row in tip_df.iterrows():
                    control = AwsEc2TipControl(
                        description=row['Control Title'],
                        remediation=row['Remediation'],
                        ics_std_reference_no=row['ICS ID'],
                        ics_control_area=row['ICS Control Area']
                    )
                    session.add(control)
                session.commit()
            
            output_file = os.path.join(output_folder, os.path.basename(tip_file))
            tip_df.to_excel(output_file, index=False)
            print(f"Processed and saved {tip_file} to {output_file}")
        except Exception as e:
            print(f"Error processing {tip_file}: {e}")

if __name__ == "__main__":
    tip_folder
