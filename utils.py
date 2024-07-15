def map_control_title_to_l2_id(self, control_title: str) -> str:
        try:
            row = self.aws_df[self.aws_df['L4 Control Name'] == control_title]
            if row.empty:
                raise ValueError(f"Control title '{control_title}' not found in AWS data.")
            return row.iloc[0]['L2 ID']
        except Exception as e:
            print(f"Error mapping control title to L2 ID: {e}")
            return None
    
    def map_l2_id_to_control_domain(self, l2_id: str) -> str:
        try:
            row = self.master_df[self.master_df['Statement index'] == l2_id]
            if row.empty:
                raise ValueError(f"L2 ID '{l2_id}' not found in Master data.")
            return row.iloc[0]['Control Domain']
        except Exception as e:
            print(f"Error mapping L2 ID to Control Domain: {e}")
            return None
