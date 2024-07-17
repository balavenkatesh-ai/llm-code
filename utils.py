def get_aws_ec2_tip_controls() -> List[AwsEc2TipControl]:
    """
    Retrieve data from the AwsEc2TipControl table.

    Returns:
        A list of AwsEc2TipControl objects.
    """
    try:
        # Using the 'with' statement to ensure the session is closed properly
        with SessionLocal() as session:
            # Query the table
            controls = session.query(AwsEc2TipControl).all()
            return controls
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
