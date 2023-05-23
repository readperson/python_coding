def design_case(design_case_lists):
        design_case_lists = list(set(design_case_lists))
        design_case_lists.sort()
        print("design_case_lists 共有", len(design_case_lists), "个")
        design_case_lists = str(design_case_lists)
        design_case = "design_case_id.txt"
        with open(design_case, "w", encoding="utf-8") as f:
            f.write(design_case_lists)
