
shit_list_pref = ["Mr.",
                  "Ms.",
                  "Mrs.",
                  "Dr.",
                  "Hon.",
                  "Hon",
                  "Min.",
                  "The",
                  "Rt.",
                  "Right",
                  "Honourable",
                  "Honorable",
                  "Admiral",
                  "VAdm.",
                  "Senator",
                  'Minister',
                  'Monsieur',
                  "L'honorable",
                  "L’honorable",
                  "Honoruable",
                  "Honorable/Honorable",
                  "Hon.)",
                  "(The",
                  "L'hon.",
                  "l'hon",
                  "Ho.",
                  "CFNE",
                  "P.C.,M.P.",
                  "L'Hhonorable",
                  "H.E.",
                  "His",
                  "Excellency",
                  "Commodore",
                  "LGen",
                  "Major",
                  "General",
                  "Brigadier-General",
                  "Brigadier",
                  "Vice",
                  "Admiral",
                  "Rear-Admiral",
                  '']

shit_list_suff = ["P.C.",
                  "M.P.",
                  "P.C",
                  "M.P",
                  "MP",
                  "PC",
                  "Ph.D",
                  "PhD",
                  "MA",
                  "M.A.",
                  "Manager",
                  "Policy",
                  "Director"]


shit_list_pref_lower = [x.lower() for x in shit_list_pref]
shit_list_suff_lower = [x.lower() for x in shit_list_suff]
shit_list_combined = shit_list_pref_lower.copy()
shit_list_combined.extend(shit_list_suff_lower)


first_name_synonyms = {'Alexander': ['Alex'],
                       "James": ['Jim', "Jimmy"],
                       "Kathleen": ['Kathy'],
                       'Micheal': ['Mike'],
                       'William': ['Bill']}

most_proper = ['Alexander', 'James', 'Kathleen', 'Micheal', 'William']
