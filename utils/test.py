from utils.email_utils import send_job_email

test_job = {
    "title": "TEST JOB",
    "ai_recommendation_1_10": 9,
    "job_id": 2,   # létező jobs.id a DB-ben!
    "desc" : "Test Engineer (Intern) on Industrial Automation Field Today the community of around 1800 IT professionals and engineers believe - along with me - that the evosoft team is the place for us. Our co-workers in Budapest, Miskolc and Szeged are busy writing software which, although invisible to the naked eye, can fundamentally influence the very basics of our everyday lives. You will come across our software solutions in different kinds of the largest medical equipment technology, not to mention that our codes drive the greatest car manufacturers’ automation systems and you can even find them/us in electric cars. There are hardly any industrial areas where the programs I and my colleagues tested or developed are not present. The company evosoft, in its full name evosoft Hungary Kft. (Ltd.) started with 3 members more than 30 years ago. As of today, our headcount has reached the 1800 employees and we are expanding - join us, be part of our team!",
    "link" : "https://muisz.hu/diakmunkaink/test-engineer-%20Industrial-Automation-Field-trainee-xi-kerulet--28375",
    "wage" : "2000"
}
send_job_email(test_job)