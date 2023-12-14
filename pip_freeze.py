import pkg_resources

# Get list of installed packages and their versions
installed_packages = pkg_resources.working_set
installed_packages_list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])

# Write the list to a text file
with open("installed_packages.txt", "w") as f:
    f.write("\n".join(installed_packages_list))