from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy,request
import datetime
import pytz
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:aEzES_9wESCUhhJ4@devinstance.cmmaelkfp8je.ap-south-1.rds.amazonaws.com/medidata'
app.debug = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)


last_updated_date = datetime.datetime.now(pytz.timezone('Asia/Calcutta'))
last_updated_date = last_updated_date.strftime("%Y-%m-%d %H:%M:%S")
last_updated_date = "'" + last_updated_date + "'"

def input_validator(data):
    #check ptient visit id
    visit_id = data.get('visit_id')
    id = data.get('id')

    if id:
        try:
            str(id)
        except ValueError as e:
            return False,'id is not string'
    else:
        return False,'id key not found' # to make input compulsurry
    if visit_id:
        try:
            int(visit_id)
        except ValueError as e:
            return False,'visit_id is not integer'
    else:
        return False, 'visit_id key not found' # to make input compulsurry

    return True,True



@app.route('/inputdata',methods=['POST'])

def input():
    input_data = request.get_json()
    id_ = input_data.get('id')

    visitid_ = input_data.get('visit_id')
    check,message = input_validator(input_data)
    if not check:
        return message
    if id_ and visitid_ and isinstance(id_,str):
        user_= Authors.query.filter_by(user_id=id_).first()
        if user_:
            print(user_.role_id)
            if user_.role_id in [4,5]:
                health = PHS.query.filter_by(patient_visit_id=visitid_).first()
                print('&&&&&&',health.manual_patient_health_score)
                if health:
                    if input_data.get('manual_patient_health_score') != 'null':
                        health.manual_patient_health_score =input_data.get('manual_patient_health_score')
                    else:
                        health.manual_patient_health_score = health.past_health_score

                    if input_data.get('manual_reports_health_score') != 'null':
                        health.manual_reports_health_score = input_data.get('manual_reports_health_score')
                    else:
                        health.manual_reports_health_score = health.reports_health_score

                    if input_data.get('manual_assessment_health_score') != 'null':
                        health.manual_assessment_health_score = input_data.get('manual_assessment_health_score')
                    else:
                        health.manual_assessment_health_score = health.assessment_health_score

                    # print('A:',health.manual_assessment_health_score)
                    # print('B:', health.manual_reports_health_score)
                    # print('C:', health.manual_patient_health_score)

                    u_score = 1.0 * int(health.manual_assessment_health_score) + 1.4 * int(health.manual_reports_health_score) + 1.2 * int(health.manual_patient_health_score)
                    health.health_score = u_score
                    health.last_updated_by = input_data.get('id')
                    health.last_updated_date = last_updated_date
                    db.session.commit()
                    return 'data updated'
                else:
                    return 'patient visit_id not found'
            else:
                return 'you are not authorised'
        else:
            return "user id not existed in auth table"
    return 'Failed'




class Authors(db.Model):
    __table_args__ = {'schema':'medidata'}
    __tablename__ = 'auth_users'
    user_id = db.Column(db.String(100),primary_key =True)
    role_id = db.Column(db.String(100))

    def __init__(self,user_id,role_id):

        self.user_id = user_id
        self.role_id = role_id


class PHS(db.Model):
    __table_args__ = {'schema':'medidata'}
    __tablename__ = 'patient_health_score'
    health_score_id = db.Column(db.String(100),primary_key =True)
    patient_visit_id = db.Column(db.Integer())
    past_health_score = db.Column(db.Integer())
    reports_health_score = db.Column(db.Integer())
    assessment_health_score = db.Column(db.Integer())
    health_score = db.Column(db.Integer())
    status = db.Column(db.Integer())
    created_date = db.Column(db.DateTime(timezone=True))
    created_by = db.Column(db.String(100))
    last_updated_date = db.Column(db.DateTime(timezone=True))
    last_updated_by = db.Column(db.DateTime(timezone=True))
    manual_patient_health_score = db.Column(db.Integer())
    manual_reports_health_score = db.Column(db.Integer())
    manual_assessment_health_score = db.Column(db.Integer())
    after_approval_change = db.Column(db.String(100))


    def __init__(self,health_score_id,patient_visit_id,past_health_score,reports_health_score,assessment_health_score,health_score,status,created_date,created_by,last_updated_date,last_updated_by,manual_patient_health_score,manual_reports_health_score,manual_assessment_health_score,after_approval_change):

        self.health_score_id = health_score_id
        self.patient_visit_id = patient_visit_id
        self.past_health_score = past_health_score
        self.reports_health_score = reports_health_score
        self.assessment_health_score = assessment_health_score
        self.health_score = health_score
        self.status = status
        self.created_date = created_date
        self.created_by = created_by
        self.last_updated_date = last_updated_date
        self.last_updated_by = last_updated_by
        self.manual_patient_health_score = manual_patient_health_score
        self.manual_reports_health_score = manual_reports_health_score
        self.manual_assessment_health_score = manual_assessment_health_score
        self.after_approval_change = after_approval_change










@app.route('/Phscore',methods=['GET'])
def phscores():

    scores = PHS.query.all()
    output = []
    for score in scores:
        currauth = {}
        currauth['health_score_id'] = score.health_score_id
        currauth['patient_visit_id'] = score.patient_visit_id
        currauth['past_health_score'] = score.past_health_score
        currauth['reports_health_score'] = score.reports_health_score
        currauth['assessment_health_score'] = score.assessment_health_score
        currauth['health_score'] = score.health_score
        currauth['status'] = score.status
        currauth['created_date'] = score.created_date
        currauth['created_by'] = score.created_by
        currauth['last_updated_date'] = score.last_updated_date
        currauth['last_updated_by'] = score.last_updated_by
        currauth['manual_patient_health_score'] = score.manual_patient_health_score
        currauth['manual_reports_health_score'] = score.manual_reports_health_score
        currauth['manual_assessment_health_score'] = score.manual_assessment_health_score
        currauth['after_approval_change'] = score.after_approval_change



        output.append(currauth)
    return jsonify(output)






@app.route('/get_authors',methods=['GET'])
def authorsd():

    all_authors = Authors.query.all()
    # print(all_authors)
    output = []
    for auth in all_authors:
        currauth={}
        currauth['user_id'] = auth.user_id
        currauth['role_id'] = auth.role_id

        output.append(currauth)
    return jsonify(output)

