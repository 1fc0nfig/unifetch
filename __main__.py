import requests
import json
import argparse
import re

# initialize argument parser
parser = argparse.ArgumentParser(description='Download all answers from a course')
parser.add_argument('-c', '--course_id', required=False, help='The course id to download answers from')

# parse arguments
args = parser.parse_args()
course_id = args.course_id

# main runtime
def main(course_id):
    return 0

# function that parses course data and extracts lesson ids
def get_lesson_ids(course_data):
    # parse lesson data as json
    course_json = json.loads(course_data)
    # extract lesson ids (topics)
    topics = []

    try:
        for x in course_json['course']['blockList']:
            for y in x['topicList']:
                for z in y['lessonCodeList']:
                    topics.append(z)
    except Exception as e:
        print(f'Could not extract lesson ids: {e}')
        pass

    return topics

# parses correct answers from lesson data
def parseLessonData(data):
    for i in data.items():
        if i[0] == 'questionMap':
            for j in i[1].items():
                try:
                    print(j[0])

                    task = j[1]['task']['cs']

                    answerList = []
                    pairAnswerList = []
                    correctAnswerIndexes = []
                    correctAnswerOrder = []
                    correctAnswers = []

                    if 'pairList' in j[1].keys():
                        for l in j[1]['pairList']:
                            pairAnswerList.append(l)

                    if 'answerList' in j[1].keys():
                        for k in j[1]['answerList']:
                            # print(type(k))
                            try:
                                if type(k) == dict:
                                    try:
                                        answerList.append(k['cs'])
                                    except:
                                        answerList.append(k)

                                elif type(k) == list:
                                    answerList.append(k)
                                    pass
                                elif type(k) == str:
                                    answerList.append(k)
                                    pass
                                elif type(k) == int:
                                    answerList.append(k)
                                    pass
                            
                            except Exception as e:
                                print(k)
                                print(type(k))
                                raise Exception(f"Unknown type ❌: {e}")
                                pass

                    if 'correctAnswerIndexList' in j[1].keys():
                        for l in j[1]['correctAnswerIndexList']:
                            correctAnswerIndexes.append(l)

                    if 'correctAnswerIndex' in j[1].keys():
                        correctAnswerIndexes.append(j[1]['correctAnswerIndex'])

                    # correctAnswerOrder
                    if 'correctAnswerOrder' in j[1].keys():
                        correctAnswerOrder = j[1]['correctAnswerOrder']

                    # print(answerList)
                    # print(correctAnswerIndexes)

                    # extract correct answers
                    if not pairAnswerList:
                        if len(answerList) > 0:
                            if type(answerList[0]) == list:
                                for x in range(len(correctAnswerIndexes)):
                                    try:
                                        correctAnswers.append(answerList[int(x)][int(correctAnswerIndexes[int(x)])]['cs'])
                                    except Exception as e:
                                        try:
                                            correctAnswers.append(answerList[int(x)][int(correctAnswerIndexes[int(x)])])
                                        except Exception as e:
                                            raise e
                            elif not correctAnswerOrder:
                                for m in correctAnswerIndexes:
                                    correctAnswers.append(answerList[m])
                            else:
                                for m in correctAnswerOrder:
                                    correctAnswers.append(answerList[m])
                        else:
                            correctAnswers.append(True) if correctAnswerIndexes[0] == 0 else correctAnswers.append(False)

                    # remove UU Shit
                    # task = remove_UUshit(task)
                    print(task)

                    for x in correctAnswers:
                        # x = remove_UUshit(str(x))
                        x = x.replace('\n', '') if type(x) == str else x
                        print(f"\t {x}")
                    print('------------------------------------------------------------------------------------------------------------------------------')
                    pass
                except Exception as e:
                    print('Caught exception: ' + str(e))
                    pass
            pass
        pass
    pass

# get raw course data by its id
def get_course_data(course_id):
    # Paste in parsed request here:
    # # # # # # # # # # # # # # # # # # # # # # # #
    cookies = {
        'uu.app.s': '1651693986.YXQuTTZpVnNQS2ZocmdTS25ZVy1QbklzWGR0SFJ1aVNmb1RNbkZkMHFpU0l1MA.1651723317.ZDcxZTI2ZDdlNWZiYzMzN2MxYzgxODE5YzVlZDNmOWZjMTFhNjcyMzEwODdiZDVjYzE3NDVkNjEzMDQ1MTkwNi5ncWJoUXJpSS1DNnZVR2VsaXdUNDR4M3poeGprR3RKOFlXM28tOWUyOEcw.3d14b794997048bfa5a446a26777ab02',
        'uu.app.csrf': '1651693986.f74b3a8e56560981f85ddc04c173c84b08b541e5.34ba8f1ee4aff0844aca4c899c63baae',
        '_ga': 'GA1.2.1252016071.1629108802',
        '_ga_PF1RBZ7QBT': 'GS1.1.1629108903.1.1.1629109113.0',
    }

    headers = {
        'authority': 'uuapp.plus4u.net',
        'accept': 'application/json',
        'accept-language': 'cs,en;q=0.9,sk;q=0.8',
        'cache-control': 'no-cache',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'uu.app.s=1651693986.YXQuTTZpVnNQS2ZocmdTS25ZVy1QbklzWGR0SFJ1aVNmb1RNbkZkMHFpU0l1MA.1651723317.ZDcxZTI2ZDdlNWZiYzMzN2MxYzgxODE5YzVlZDNmOWZjMTFhNjcyMzEwODdiZDVjYzE3NDVkNjEzMDQ1MTkwNi5ncWJoUXJpSS1DNnZVR2VsaXdUNDR4M3poeGprR3RKOFlXM28tOWUyOEcw.3d14b794997048bfa5a446a26777ab02; uu.app.csrf=1651693986.f74b3a8e56560981f85ddc04c173c84b08b541e5.34ba8f1ee4aff0844aca4c899c63baae; _ga=GA1.2.1252016071.1629108802; _ga_PF1RBZ7QBT=GS1.1.1629108903.1.1.1629109113.0',
        'pragma': 'no-cache',
        'referer': 'https://uuapp.plus4u.net/uu-coursekit-courseg01/286a85d928da49ebb60816c715ae15dc/course/courseWelcome',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36',
        'x-csrf-token': '1651693986.f74b3a8e56560981f85ddc04c173c84b08b541e5.34ba8f1ee4aff0844aca4c899c63baae',
        'x-request-id': '623df35e-623df35e-4cf6d4b9-0000',
    }

    response = requests.get('https://uuapp.plus4u.net/uu-coursekit-courseg01/286a85d928da49ebb60816c715ae15dc/loadCourseForStudent', cookies=cookies, headers=headers)

    # # # # # # # # # # # # # # # # # # # # # # # #
    error_json = json.loads(response.text)
    print('uuAppErrorMap: ', error_json['uuAppErrorMap'])

    if error_json['uuAppErrorMap'] != '':
        return response.text
    else:
        raise Exception(f'Could not get course data: {response.status_code}, {response.text}')

# get raw lesson data by its id
def get_lesson_data(lesson_id):
    # Paste in parsed request here:
    # # # # # # # # # # # # # # # # # # # # # # # #
    import requests

    cookies = {
        'uu.app.s': '1651792737.YXQud1BaaXJzamFNV0dKNk1lWFRvV245c2NHRWhTem5SaGlnSHRjUE1TeFRRRQ.1651808968.OTQ1MGI0MzkzZmZkYmVmZDQwYTlkYTUxYmFmMDlhNDRhNWU4M2VlNmMzODBiMjgzM2FhZDAxZjhiYjQ0ZDNlYy5QR0h3VzJNSEc3SjZZNk9nOXdla0ZtS2RIb3c3cjlyY2dXWVE3R0Z1NU5Z.3d14b794997048bfa5a446a26777ab02',
        'uu.app.csrf': '1651792737.982628a6499912f7bd56368dbcb1f44f01ab58a5.b80de7969eacb39fa5f829c2ec6466c4',
        '_ga': 'GA1.2.1252016071.1629108802',
        '_ga_PF1RBZ7QBT': 'GS1.1.1629108903.1.1.1629109113.0',
    }

    headers = {
        'authority': 'uuapp.plus4u.net',
        'accept': 'application/json',
        'accept-language': 'cs,en;q=0.9,sk;q=0.8',
        'cache-control': 'no-cache',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'uu.app.s=1651792737.YXQud1BaaXJzamFNV0dKNk1lWFRvV245c2NHRWhTem5SaGlnSHRjUE1TeFRRRQ.1651808968.OTQ1MGI0MzkzZmZkYmVmZDQwYTlkYTUxYmFmMDlhNDRhNWU4M2VlNmMzODBiMjgzM2FhZDAxZjhiYjQ0ZDNlYy5QR0h3VzJNSEc3SjZZNk9nOXdla0ZtS2RIb3c3cjlyY2dXWVE3R0Z1NU5Z.3d14b794997048bfa5a446a26777ab02; uu.app.csrf=1651792737.982628a6499912f7bd56368dbcb1f44f01ab58a5.b80de7969eacb39fa5f829c2ec6466c4; _ga=GA1.2.1252016071.1629108802; _ga_PF1RBZ7QBT=GS1.1.1629108903.1.1.1629109113.0',
        'pragma': 'no-cache',
        f'referer': 'https://uuapp.plus4u.net/uu-coursekit-courseg01/286a85d928da49ebb60816c715ae15dc/course/lesson?code={lesson_id}',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36',
        'x-csrf-token': '1651792737.982628a6499912f7bd56368dbcb1f44f01ab58a5.b80de7969eacb39fa5f829c2ec6466c4',
        'x-request-id': '623df35e-623df35e-50268296-0000',
    }

    params = {
        'code': f'{lesson_id}',
    }

    response = requests.get('https://uuapp.plus4u.net/uu-coursekit-courseg01/286a85d928da49ebb60816c715ae15dc/loadLessonForStudent', params=params, cookies=cookies, headers=headers)
    # # # # # # # # # # # # # # # # # # # # # # # #
    
    error_json = json.loads(response.text)
    print(f"Lesson ID: {lesson_id}; Status: [{response.status_code}], uuAppErrorMap: {error_json['uuAppErrorMap']}")

    if error_json['uuAppErrorMap'] != '':
        return response.text
    else:
        raise Exception(f'Could not get lesson data: {response.status_code}, {response.text}')


# Test id

# course_id = '286a85d928da49ebb60816c715ae15dc' 
# course_data = get_course_data(course_id)
# lesson_ids = get_lesson_ids(course_data)

lesson_ids = ['LC_0002', 'LC_0003', 'LC_0004', 'LC_0005', 'LC_0006', 'LC_0007', 'LC_0008', 'LC_0009', 'LC_0010', 'LC_0011', 'LC_0012', 'LC_0013', 'LC_0014', 'LC_0015', 'LC_0016', 'LC_0017', 'LC_0018', 'LC_0019', 'LC_0020', 'LC_0021', 'LC_0022', 'LC_0023', 'LC_0024', 'LC_0025', 'LC_0026', 'LC_0027', 'LC_0028', 'LC_0029', 'LC_0030', 'LC_0031', 'LC_0032', 'LC_0033', 'LC_0034']

for lesson in lesson_ids:
    try:
        lesson_data = get_lesson_data(lesson)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
    parseLessonData(json.loads(lesson_data))

