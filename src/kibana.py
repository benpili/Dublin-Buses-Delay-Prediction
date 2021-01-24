from datetime import datetime


def create_link(time1: datetime, time2: datetime):
    time1_str = time1.strftime("'%Y-%m-%dT%H:%M:%S.%fZ'")
    time2_str = time2.strftime("'%Y-%m-%dT%H:%M:%S.%fZ'")
    return "http://da2020w-0009.eastus.cloudapp.azure.com:5601/app/dashboards#/view/69bba470-54de-11eb-94d1-e919c49" \
           "ef164?_g=(filters:!(),refreshInterval:(pause:!t,value:0),time:(from:{},to:{}))&_a=(description:'',filte" \
           "rs:!(),fullScreenMode:!f,options:(hidePanelTitles:!f,useMargins:!t),query:(language:kuery,query:'')," \
           "timeRestore:!f,title:Project,viewMode:view)".format(time1_str, time2_str)


if __name__ == '__main__':
    print(create_link(datetime.now(), datetime.now()))
