# Overview of the Yoda group-manager
The Yoda group-manager is a central tool for all Yoda implementations. The group-manager is used to control access permissions of users based on group membership and the role inside a group. As this usecase is not fully anticipated in the iRODS ACL (Access Control List) system, the group-manager makes use of shadow groups and metadata to accomplish its goals. To understand the choices made in the group-manager you need to understand the limitations of iRODS.


The main goal of the group-manager is to enable the distribution of access rights to data within Yoda with minimal aid of the Yoda administrators. All data within Yoda belongs to a group within a community and access is granted by group membership and roles.

## Yoda roles
normal
> Has read and write access to the data of the group it belongs to. Most researchers will be assigned this role.

reader
> Has read access to the data. This role could be assigned to users with interest in the data like master students.

groupmanager

> Can add users to a group and assign them roles. Every group should have at least one groupmanager. This role is typically assigned to a principal investigator.


datamanager
> Has read access to data belonging to his/her community and the ability to manage archival process and metadata quality.


## Yoda workspaces
Within a Yoda community multiple workspaces can be created of different types. They are prefixed to indicate this type. Every workspace is located in the /{rodsZone}/home collection. Davrods and the research browser have this location as start location.

research
> Collaboration workspace for a research group. No restrictions on the organization of data in folders. Metadata can be added to a folder. When all required metadata has been added a folder can be archived.

intake
> A strict folder structure and filename structure is required to extract metadata and archive data in an intake workspace.

grp
> Legacy workspaces are prefixed with grp-. They were created before the development of research workspaces. The current group-manager will prohibit the creation of new grp groups, but supports managing existing ones.


## Category and subcategories
To allow different communities to share the same Yoda implementation the concept of categories and subcategories were introduced. Every group has a category and subcategory. Within the group-manager groups are grouped into a tree of categories and subcategories.

## The iRODS permission system
1. iRODS has four user types:
	- rodsuser, a normal user
	- rodsadmin, a superuser which can invoke commands in admin mode.
	- groupadmin, a user capable of adding other users to groups it belongs to. Not used by Yoda
	- rodsgroup, a group of users. Permissions granted to a rodsgroup apply to it's members.
2. A Group is also a user. In the iRODS datamodel they share a table. Groups have a separate table to list members.
3. A group can not include another group. The hierarchy is flat. Groups have users as members, users can join multiple groups.
4. Permissions on Collections and DataObjects are either 'own', 'write' or 'read' set per user (a group is a user in this context). own has write, write implies read.
5. Group permissions set on collections only apply on subcollections if "inherit" is set.
6. iRODS allows federation of users between zones. To distinguish between local users and users from other zones, every query involving users should include the zone name.  Users from different zones can be represented by appending a # and the zonename to the username. Example: myuser becomes myuser#myzone


## The sudo microservices
To enable ordinary rodsusers to create groups and manage members in groups, without promoting them to rodsadmin, the sudo microservices have been developed. They give temporary admin privileges when an action meets all criteria set in policies. Technically this means that a sudo microservice will set the AUTH flags in the iRODS rei structure to run an action as admin. Care is taken to prevent the use of these services outside of the proper context.


## How are the roles in yoda implemented on top of the iRODS permission system?
*Normal* users are added to a group with the same name as its workspace. Example: normal users of *research-breakthrough* are added to the rodsgroup *research-breakthrough*. During group creation by the group-manager this group will get permission 'own' on the /{rodsZone}/home/research-breakthrough workspace and inheritance is enabled.

A *reader* cannot be added to the main group, because that will grant them 'own' permissions. Instead a shadow group is created prefixed with 'read-'. This group gets read permissions on the 'research-' or 'intake-' group of the same basename. Inheritance is enabled

A group *manager* has all the same characteristics as a normal user but in addition metadata is set on the group to list managers. The attribute name is 'manager' and the attribute value is the username (including zone). There are two special groups under the System category to grant managers extra privileges. These are:
  - *priv-group-add* --
    Membership of this group is checked to determine if a user can create groups. The user also needs to be manager in one of the groups belonging to the same category.

  - *priv-category-add* --
    Members of this group can create new categories. This is done when a new group is created. Because categories are implemented as metadata on groups, removing all groups from a category removes that category.

A *datamanager* is not a member of a group belonging to a workspace. Instead a special 'datamanager-' group needs to be created per category. This group has to have the same name as that category. This group is given read access to every workspace in this category. This allows the datamanager to check the quality of data and metadata before archiving the work.

## iRODS ruleset
The following files in the irods-ruleset-uu support the groupmanager.

uuSudoPolicies
> Set of policies for every sudo action. Every action is denied by default.

uuGroupPolicies
> Policies specific for actions related to the group manager. They have been specified seperately so the rules in uuSudoPolicies can be kept as simple as possible

uuGroupPolicyChecks
> Can be used by the portal and by rules. Queries related to policies

uuGroup
> Can be used by the portal and by policies. It contains the queries used directly by th Group Manager. Policies should not be used directly by the group manager.

The files represent layers when calling functions.

uuSudoPolicies -> uuGroupPolicies -> uuGroupPolicyChecks -> uuGroup

uuGroup (Group manager portal functions) -> uuGroupPolicyChecks


## Users and groups
Users and groups are in same namespace, so checks are in place to prevent creating a group with the same name as a user.


## Vault
The vault group has only rods as member. the base group should get read-only access. Removal of a vault group through the group-manager is impossible.
