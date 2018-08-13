### Sysbot
By - Sammy1997  
Mentors: Ramit Sawhney, Akshita Aggarwal  
Admin: Prachi Manchanda  

### Design for Template matching
**June 02, 2018**  

Following are the links to a sample issue which follows the template
and the body of the issue as sent to the
server by the web-hook:  

[Issue](https://github.com/systers/sysbot-test/issues/48)  
[Response](https://dpaste.de/Pb7x)  

So basically the task is to search in the body of the issue,
for the presence of these headers :  

1. **Description**
2. **Acceptance Criteria** - followed by “Update” or “Update [Required]”
3. **Definition of Done**
4. **Estimation**  

We are not considering **Mocks and Enhancements** as they are optional
and may or may not be present.  

When we use these [lines of code](https://dpaste.de/ZGAj) on this [Response](https://dpaste.de/Pb7x) , we get the following [tokens](https://dpaste.de/jRDh).  

From this final curated list of tokens,
we need to iterate through the tokens and search for the above given words in the tokens in each run.  

If all are present, along with some text in the next token then we can say that this is a valid template.  

I would like to discuss the course of action that is to be taken if invalid issues are found.  

As per discussion with the community, the bot would add a ***label of “Template Mismatch” to them***,
so that the mentors/admins/maintainers could see all the issues by searching by this label,
and then they will be ***closed manually***. Also, ***any issue labelled "Template Mismatch"  can't be approved, assigned or claimed***.
