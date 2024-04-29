import { Formik, Form, Field, FormikHelpers, FormikConfig } from "formik";
import { Select, SelectItem } from "@nextui-org/react";
import * as Yup from "yup";

const MainReportFilterComponent = () => {
  const validationSchema = Yup.object().shape({
    projectName: Yup.string().required("Project name is required"),
    selectedUsers: Yup.array().min(1, "Please select at least one user"),
  });

  interface FormValues {
    projectName: string;
    allUsers: string[];
    selectedUsers: string[];
  }
  const handleSubmit = async (
    values: FormValues,
    actions: FormikHelpers<FormValues>
  ): Promise<void> => {
    console.log(values);
  };

  return (
    <Formik
      initialValues={{
        projectName: "",
        allUsers: [],
        selectedUsers: [],
      }}
      validationSchema={validationSchema}
      onSubmit={(values, actions) => {
        handleSubmit(values, actions as FormikHelpers<FormValues>);
      }}
    >
      {({ values, setFieldValue, errors, touched }) => (
        <Form>
          <div>
            <label htmlFor="projectName">Project Name:</label>
            <Field
              as={Select}
              name="projectName"
              error={touched.projectName && errors.projectName}
              onChange={(e) => {
                // Set project name and reset selected users
                const projectName = e.target.value;
                const dummyUsers = ["User 1", "User 2", "User 3"];
                setFieldValue("selectedUsers", []);
                setFieldValue("projectName", projectName);
                setFieldValue("allUsers", dummyUsers);
              }}
            >
              <SelectItem key={0} value="">
                Select Project
              </SelectItem>
              <SelectItem key={1} value="project1">
                Project 1
              </SelectItem>
              <SelectItem key={2} value="project2">
                Project 2
              </SelectItem>
              <SelectItem key={3} value="project3">
                Project 3
              </SelectItem>
            </Field>
            {touched.projectName && errors.projectName && (
              <div className="error">{errors.projectName}</div>
            )}
          </div>

          {/* Conditionally render user input if project is selected */}
          {values.projectName && (
            <div>
              <label htmlFor="selectedUsers">Users:</label>
              <Field
                as={Select}
                name="selectedUsers"
                isRequired
                label="Favorite Animal"
                placeholder="Select an animal"
                variant="bordered"
                className="max-w-xs"
                selectionMode="multiple"
                error={touched.selectedUsers && errors.selectedUsers}
                errorMessage={
                  touched.selectedUsers && errors.selectedUsers
                    ? ""
                    : errors.selectedUsers
                }
                isInvalid={
                  touched.selectedUsers && errors.selectedUsers ? true : false
                }
                onChange={(e) => {
                  setFieldValue("selectedUsers", e.target.value.split(","));
                  console.log("F1", e.target.value);
                  console.log("F2", Array.from(e.target.value));
                  console.log("F3", values.selectedUsers);
                }}
              >
                {values.allUsers.map((user, i) => (
                  <SelectItem key={user} value={user}>
                    {user}
                  </SelectItem>
                ))}
              </Field>
            </div>
          )}

          <button type="submit">Submit</button>
        </Form>
      )}
    </Formik>
  );
};

export default MainReportFilterComponent;
