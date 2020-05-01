"""
COMPANIES USING WORKDAY SOFTWARE

@author:    Gerard Mazi
@date:      2020-04-27
@email:     gerard.mazi@gmail.com
@phone:     862-221-2477

"""

import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import re
import matplotlib.pyplot as plt



'=============================================================='

time_stamp = pd.to_datetime('2020-04-30')

userid = 'gerard.mazi@gmail.com'
password = 'Geruci0203'
'=============================================================='

driver = webdriver.Chrome(r"chromedriver.exe")

driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
time.sleep(2)

# Login
driver.find_element_by_xpath('//*[@id="username"]').send_keys(userid)
driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
driver.find_element_by_xpath('//*[@class="btn__primary--large from__button--floating"]').click()
time.sleep(3)

# Run above first
#######################################################################################################################

comps = pd.read_csv('in_Comp.csv').values.tolist()
wday_temp = pd.DataFrame({'Date': [], 'Comp': [], 'Test': []})

# Go to company and jobs
for c in range(len(comps)):

    driver.get(comps[9][0])
    time.sleep(3)

    # Company name
    t_comp = driver.find_element_by_xpath('//*[@class="org-top-card-summary__title t-24 t-black truncate"]').text

    try:
        # Open a role
        driver.find_element_by_xpath('//*[@class="artdeco-carousel ember-view"]/div[2]/ul/li[2]').click()
        time.sleep(3)

        # Click on apply
        driver.find_element_by_xpath('//*[@class="jobs-apply-button--top-card ember-view"]').click()
        time.sleep(7)

        # Switch to the new tab opened
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(1)

        # Get Workday footer
        try:
            t_test = driver.find_element_by_xpath('//*[@class="gwt-HTML WJ2P"]').text
        except:
            t_test = ''

        # Close tab
        driver.close()

        # Switch back to initial tab
        driver.switch_to.window(driver.window_handles[0])

    except:
        t_test = ''

    temp = pd.DataFrame({'Date': [time_stamp], 'Comp': [t_comp], 'Test': [t_test]})

    wday_temp = pd.concat([wday_temp, temp], ignore_index=True)












#######################################################################################################################
# Convert to integer
role_temp['Count'] = role_temp['Count'].str.replace(',', '').astype(int)

# Append to stored jobs
roles = pd.concat([roles, role_temp], axis=0, ignore_index=True)
roles.to_pickle('store_roles.pkl')

#######################################################################################################################
# ANALYTICS

val = [
    'Product Management', 'Program and Project Management', 'Finance', 'Marketing', 'Human Resources',
    'Consulting', 'Operations', 'Support', 'Information Technology', 'Engineering', 'Business Development', 'Sales'
]
dat = roles[roles.Date == time_stamp]
tab = pd.crosstab(dat.Comp, dat.Role, dat.Count, aggfunc=np.sum, normalize='index')
for v in val:
    plt.figure(figsize=(10, 6)).tight_layout()
    tab[v].sort_values().plot(kind='bar', title=v)
    plt.show()