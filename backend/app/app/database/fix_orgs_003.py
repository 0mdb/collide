from schema_creation.sqlmodel_build import Organization, \
    OrganizationType
from sqlmodel import select
import common_func as cf
import fix_funcs

sess = cf.create_session(debug=False)
actually_do_it = True

sql_query = select(Organization)
res_all_orgs = sess.exec(sql_query).all()

for each_org in res_all_orgs:
    name_in_question = each_org.match_name
    preferred_match_name = fix_funcs.return_preferred_party_name(name_in_question)

    if preferred_match_name == -1:
        # then it's not a recognized party name
        continue
    else:
        # recognized as a party name
        sql_query = select(Organization).where(Organization.match_name == preferred_match_name)
        keeper_org = sess.exec(sql_query).first()
        keeper_id = keeper_org.id
        print(f"we are going to keep {keeper_org.display_name} (id {keeper_id})")

        # update keeper organization_type = political party
        stat = select(OrganizationType.id).where(
            OrganizationType.match_name == "politicalparty"
        )
        type_party_id = sess.exec(stat).first()

        keeper_org.organization_type = type_party_id

        # update keeper parent_organization = federalgovernmentofcanada
        stat = select(Organization.id).where(
            Organization.match_name == "federalgovernmentofcanada"
        )
        fed_id = sess.exec(stat).first()

        keeper_org.parent_organization = fed_id

        if actually_do_it:
            sess.add(keeper_org)
            sess.commit()

        if name_in_question != preferred_match_name:
            print(f"\tthe following organization should be eliminated: {each_org.display_name} (id {each_org.id})")

            fix_funcs.replace_organization(old_id=each_org.id,
                                           new_id=keeper_id,
                                           sess=sess,
                                           actually_do_it=actually_do_it)

print("END")
sess.close()
