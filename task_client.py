
import json
import requests


if __name__=='__main__' :
    login_url='http://127.0.0.1/login?slave_machine_login_password=t4sk_s3rv3r_l0g1n_p4ssw0rd&slave_machine_ip=127.0.0.1&slave_machine_name=slave1'
    login=requests.get(login_url)
    login_result=json.loads(login.text)
    slave_machine_id=login_result['slave_machine_id']
    
#    print 'login ',login_url
#    print '->',login_result
    
    while True :
        dispatch_url='http://127.0.0.1/dispatch?slave_machine_id='+slave_machine_id
        dispatch=requests.get(dispatch_url)
        dispatch_result=json.loads(dispatch.text)

        if {}==dispatch_result :
            break

        dispatch_task=json.loads(dispatch_result['dispatch_task'])
        dispatch_task_id=dispatch_task['task_id']
        report_json={}
        
        try :
            if dispatch_task.has_key('task_list') :
                print 'Execute multiple_task :'
                print ''
                
                task_result_list=[]
                
                for task_index_ in dispatch_task['task_list'] :
                    task_index=json.loads(task_index_)
                    report_result=None
                    
                    exec(task_index['task_code'])
                    task_result_list.append(report_result)
                    
                report_json['report_result']=task_result_list
            else :
                print 'Execute single_task :'
                print ''
                
                report_result=None
                
                exec(dispatch_task['task_code'])
                
                report_json['report_result']=report_result
            report_json['report_state']='end'
        except Exception,e :
            report_json['report_except_name']=Exception
            report_json['report_exception_descript']=e.message
            report_json['report_state']='except'

#        print 'dispatch ',dispatch_url
#        print '->',dispatch_task
#        print 'exec() result ->',dispatch_task_result

        report_json_string=json.dumps(report_json)
        dispatch_url='http://127.0.0.1/report?slave_machine_id='+slave_machine_id+'&slave_machine_execute_task_id='+dispatch_task_id+'&slave_machine_report='+report_json_string
        report=requests.get(dispatch_url)
        report_result=json.loads(report.text)

#        print 'report ',dispatch_url
#        print '->',report_result
    
    logout_url='http://127.0.0.1/logout?slave_machine_id='+slave_machine_id
    logout=requests.get(logout_url)
    logout_result=json.loads(logout.text)
    
#    print 'logout ',logout_url
#    print '->',logout_result
    