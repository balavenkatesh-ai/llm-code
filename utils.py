def map_control_title(self, control_title: str) -> (str, str):
        """
        Maps the control title to the L2 ID and control domain using the AWS DataFrame.

        :param control_title: The control title to map.
        :return: A tuple containing the L2 ID and control domain if found, otherwise (None, None).
        """
        try:
            row = self.aws_df[self.aws_df['L4 Control Name'] == control_title]
            if row.empty:
                raise ValueError(f"Control title '{control_title}' not found in AWS DataFrame.")
            l2_id = row.iloc[0]['L2 ID']
            control_domain = row.iloc[0]['L2 Name']
            return l2_id, control_domain
        except Exception as e:
            print(f"Error mapping control title '{control_title}': {e}")
            return None, None


tip_df[['ICS ID', 'ICS Control Area']] = tip_df.apply(
                lambda row: pd.Series(mapper.map_control_title(row['Control Title'])), axis=1
            )
