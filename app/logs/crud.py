# from sqlalchemy.orm import Session
# from app.logs.model import RequestLog
#
# def create_request_log(db: Session, method: str, url: str, status_code: int, processing_time: float,
#                        ip_address: str = None, user_agent: str = None, request_body: str = None,
#                        response_body: str = None, headers: str = None, user_id: str = None):
#     log_entry = RequestLog(
#         method=method,
#         url=url,
#         status_code=status_code,
#         processing_time=processing_time,
#         ip_address=ip_address,
#         user_agent=user_agent,
#         request_body=request_body,
#         response_body=response_body,
#         headers=headers,
#         user_id=user_id
#     )
#     db.add(log_entry)
#     db.commit()
#     db.refresh(log_entry)
#     return log_entry
